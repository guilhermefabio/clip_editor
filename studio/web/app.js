"use strict";
const $ = (s, r = document) => r.querySelector(s);
const api = async (url, opt) => {
  const r = await fetch(url, opt);
  if (!r.ok) throw new Error((await r.text()) || r.status);
  return r.headers.get("content-type")?.includes("json") ? r.json() : r;
};
const post = (url, body) =>
  api(url, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) });
const pollJob = (id, onTick) =>
  new Promise((res, rej) => {
    const t = setInterval(async () => {
      try {
      const j = await api(`/api/job/${id}`);
      onTick?.(j);
      if (j.status === "done") { clearInterval(t); res(j); }
      if (j.status === "error") { clearInterval(t); rej(new Error(j.message)); }
      } catch (e) { clearInterval(t); rej(e); }
    }, 900);
  });

const S = { source: null, duration: 0, cutSeconds: 3.3333, score: null, candidates: [],
  shorts: [], planPath: null, musicReg: [], music: null, entryBeats: 0 };
const BPM = 144;

// ---------------------------------------------------------------- model + sources
const fmt = (x, d = 2) => (x == null || isNaN(x) ? "—" : (+x).toFixed(d));

async function loadModel() {
  const m = await api("/api/model");
  const pill = $("#modelPill");
  const panel = $("#modelPanel");
  const v = m.validation || {};

  if (!m.trained) {
    pill.textContent = "modelo: não treinado";
    pill.className = "pill bad";
  } else {
    pill.textContent = `modelo · AUC ${fmt(v.roc_auc)} · ${m.n_pos} exemplos · ${m.n_sources} fonte(s)`;
    pill.className = "pill ok";
    pill.title = `treinado ${m.trained_at}`;
  }

  const srcQty = (s) => {
    if (s.kind === "kill_clip") return "clipe de kill";
    if (s.kind === "frame_review") return `${s.pos} kill / ${s.neg} nada`;
    return `${s.cuts} cortes`;
  };
  const srcRows = (m.train_sources_on_disk || [])
    .map((s) => `<tr><td>${s.file}</td><td>${s.kind || ""}</td><td>${srcQty(s)}</td><td>${s.seconds != null ? s.seconds + "s" : "—"}${s.cached_only ? " (cache)" : ""}</td></tr>`)
    .join("");
  const blocked = ((m.training_status || {}).lotes || []).filter((l) => l.cuts_sources_missing.length);
  const blockedRows = blocked
    .map((l) => `<tr><td>${l.lote}</td><td class="warn">${l.cuts_sources_missing.join(", ")}</td><td>${l.rendered_shorts} shorts no disco</td></tr>`)
    .join("");
  const trainableLine = m.trainable
    ? `<span class="muted">Treino usa as <b>gravações brutas</b> (cortes = positivo, resto = negativo) + os <b>clipes de kill</b> de <code>clipes_kill/</code> (10–15 s, cru) + os <b>frames revisados</b> de <code>frames/kill</code>/<code>frames/nada</code> como extra. Áudio dentro. O checkbox ignora clipes de kill e frames revisados.</span>`
    : `<span class="warn">Nada treinável. Traga uma gravação com cortes aprovados (<code>projeto/edicao.json</code>) para a raiz; opcionalmente clipes crus de kill de 10–15 s em <code>clipes_kill/</code> e/ou frames revisados em <code>frames/kill</code>/<code>frames/nada</code>.</span>`;

  if (!m.trained) {
    panel.innerHTML = `<p class="warn">Modelo ainda não treinado.</p>${trainableLine}
      ${srcRows ? `<table class="src"><tr><th>fonte</th><th></th><th></th></tr>${srcRows}</table>` : ""}`;
    return;
  }

  const feats = (m.top_features || []);
  const fmax = Math.max(0.0001, ...feats.map((f) => f.importance));
  const fbars = feats
    .map((f) => `<div class="fbar"><span>${f.feature}</span><i style="width:${(f.importance / fmax) * 100}%"></i><span>${fmt(f.importance, 3)}</span></div>`)
    .join("");

  panel.innerHTML = `
    <div class="kv">
      <div><span>ROC-AUC (holdout)</span><b>${fmt(v.roc_auc)}</b></div>
      <div><span>Avg precision</span><b>${fmt(v.avg_precision)}</b></div>
      <div><span>Precisão @ ${fmt(v.evaluation_threshold ?? m.suggested_threshold, 2)}</span><b>${fmt(v.precision)}</b></div>
      <div><span>Recall @ ${fmt(v.evaluation_threshold ?? m.suggested_threshold, 2)}</span><b>${fmt(v.recall)}</b></div>
      <div><span>F1 @ ${fmt(v.evaluation_threshold ?? m.suggested_threshold, 2)}</span><b>${fmt(v.f1)}</b></div>
      <div><span>Threshold sugerido</span><b>${fmt(m.suggested_threshold, 2)}</b></div>
      <div><span>Positivos / negativos</span><b>${m.n_pos ?? "—"} / ${m.n_neg ?? "—"}</b></div>
      <div><span>Features</span><b>${m.n_features ?? (m.feature_names || []).length}</b></div>
      <div><span>Fontes de treino</span><b>${m.n_sources}</b></div>
      <div><span>Análise</span><b>${m.fps_analysis} fps</b></div>
    </div>
    <p class="muted" style="margin:10px 0 2px">
      Validação: ${v.scheme || "—"} · ${v.n_holdout || "?"} frames · treinado ${m.trained_at}
    </p>
    ${trainableLine}
    ${srcRows ? `<table class="src"><tr><th>fonte de treino</th><th>tipo</th><th>qtd</th><th>duração</th></tr>${srcRows}</table>` : ""}
    ${blockedRows ? `<h2 style="margin:14px 0 4px">Lotes bloqueados (gravação de origem sumiu)</h2>
      <table class="src"><tr><th>lote</th><th>falta</th><th></th></tr>${blockedRows}</table>` : ""}
    ${fbars ? `<h2 style="margin:16px 0 6px">Peso das features (permutation importance)</h2>${fbars}` : ""}
  `;
}

async function loadSources() {
  const list = await api("/api/sources");
  const sel = $("#source");
  const previous = S.source;
  sel.replaceChildren(...list.map((s) => new Option(
    `${s.file} — ${(s.duration / 60).toFixed(1)} min ${s.scored ? "✓" : ""}`, s.file)));
  $("#mergeSource").replaceChildren(...list.map((s) => new Option(s.file, s.file)));
  if (list.some((s) => s.file === previous)) sel.value = previous;
  onSourcePick();
}
function onSourcePick() {
  const sel = $("#source");
  if (S.source !== sel.value) {
    S.score = null; S.candidates = []; S.shorts = []; S.planPath = null;
    ["#secTimeline", "#secShorts", "#secRender", "#secReview"].forEach((id) => $(id).classList.add("hidden"));
    $("#btnRender").disabled = true;
  }
  S.source = sel.value;
  const txt = sel.selectedOptions[0]?.textContent || "";
  $("#srcInfo").textContent = txt.includes("✓") ? "ja analisado — pode agrupar direto" : "";
}

const mergeFiles = [];
let merging = false, analyzing = false;
function drawMergeList() {
  const list = $("#mergeList");
  list.replaceChildren();
  mergeFiles.forEach((file, i) => {
    const li = document.createElement("li");
    li.append(document.createTextNode(file + " "));
    for (const [label, delta] of [["↑", -1], ["↓", 1], ["Remover", 0]]) {
      const b = document.createElement("button");
      b.textContent = label; b.className = "ghost";
      b.disabled = merging || (delta !== 0 && (i + delta < 0 || i + delta >= mergeFiles.length));
      b.onclick = () => {
        if (delta) [mergeFiles[i], mergeFiles[i + delta]] = [mergeFiles[i + delta], mergeFiles[i]];
        else mergeFiles.splice(i, 1);
        drawMergeList();
      };
      li.append(b);
    }
    list.append(li);
  });
  $("#btnMerge").disabled = merging || analyzing || mergeFiles.length < 2;
  $("#btnMergeAdd").disabled = merging;
}
async function mergeVideos() {
  merging = true; drawMergeList();
  const msg = $("#mergeMsg"), bar = $("#mergeBar");
  bar.classList.remove("hidden");
  ["#source", "#btnAnalyze", "#btnReload"].forEach((id) => $(id).disabled = true);
  try {
    const { job } = await post("/api/merge", { files: [...mergeFiles] });
    const result = await pollJob(job, (j) => {
      bar.querySelector("i").style.width = `${j.progress * 100}%`;
      msg.textContent = j.message;
    });
    await loadSources();
    $("#source").value = result.result.file;
    onSourcePick();
    msg.textContent = "Vídeos unidos. Clique em Analisar para começar a edição.";
    mergeFiles.length = 0;
  } catch (e) { msg.textContent = "Erro: " + e.message; }
  finally {
    merging = false; drawMergeList();
    ["#source", "#btnAnalyze", "#btnReload"].forEach((id) => $(id).disabled = false);
  }
}

// ---------------------------------------------------------------- music track
async function loadMusic() {
  S.musicReg = await api("/api/music");
  const sel = $("#musicFile");
  sel.innerHTML = S.musicReg
    .map((m) => `<option value="${m.file}">${m.file}${m.known ? ` — ${m.bpm} BPM` : " — (estimar)"}</option>`)
    .join("");
  const def = S.musicReg.find((m) => m.file === "beat_phonk.wav") || S.musicReg[0];
  if (def) { sel.value = def.file; onMusicPick(); }
}
function regEntry(file) { return S.musicReg.find((m) => m.file === file); }
function onMusicPick() {
  const m = regEntry($("#musicFile").value);
  $("#beatResult").classList.add("hidden");
  if (!m) return;
  if (m.known) {
    S.music = { file: m.file, sha256: m.sha256, bpm: m.bpm,
      grid_offset_seconds: m.grid_offset_seconds, evidence: m.evidence, duration: m.duration };
    $("#btnBeat").classList.add("hidden");
    $("#musicInfo").textContent = `${m.bpm} BPM · grade ${m.grid_offset_seconds}s · ${m.duration}s — grade conhecida`;
  } else {
    S.music = null;
    $("#btnBeat").classList.remove("hidden");
    $("#musicInfo").textContent = `${m.file}: grade desconhecida — clique "Analisar batida" e confirme o BPM.`;
  }
}
async function analyzeBeat() {
  const m = regEntry($("#musicFile").value);
  $("#btnBeat").disabled = true;
  $("#musicInfo").textContent = "analisando batida…";
  try {
    const { job } = await post("/api/music/analyze", { file: m.file });
    const j = await pollJob(job, (x) => ($("#musicInfo").textContent = "analisando batida… " + x.message));
    const r = j.result;
    const box = $("#beatResult"); box.classList.remove("hidden");
    box.innerHTML = `<span class="muted">escolha o BPM:</span>` + r.candidates
      .map((c, i) => `<button class="ghost" data-bpm="${c[1]}" data-ph="${c[2]}">${c[1]} BPM · fase ${c[2]}s · ${c[0]}</button>`)
      .join("");
    box.querySelectorAll("button").forEach((b) =>
      b.addEventListener("click", () => {
        S.music = { file: m.file, sha256: m.sha256, bpm: +b.dataset.bpm,
          grid_offset_seconds: +b.dataset.ph, evidence: r.evidence, duration: m.duration };
        box.querySelectorAll("button").forEach((x) => (x.style.borderColor = ""));
        b.style.borderColor = "var(--accent)";
        $("#musicInfo").textContent = `${b.dataset.bpm} BPM · grade ${b.dataset.ph}s · ${m.duration}s — confirmado`;
      }));
  } catch (e) { $("#musicInfo").textContent = "erro: " + e.message; }
  finally { $("#btnBeat").disabled = false; }
}
function musicStart(track, beats) {
  const bpm = +track.bpm, grid = +(track.grid_offset_seconds || 0);
  let n = Math.max(0, beats | 0);
  while (n >= 0) {
    const st = grid + (n * 60) / bpm;
    if (st + 22 <= (track.duration || 1e9) + 0.005) return +st.toFixed(6);
    n -= 4;
  }
  return +grid.toFixed(6);
}

// ---------------------------------------------------------------- analyse
async function analyze() {
  analyzing = true;
  const bar = $("#anBar"); bar.classList.remove("hidden");
  $("#btnAnalyze").disabled = true;
  $("#source").disabled = true;
  $("#btnMerge").disabled = true;
  $("#btnReload").disabled = true;
  try {
    const { job } = await post("/api/analyze", { file: S.source });
    await pollJob(job, (j) => {
      bar.querySelector("i").style.width = j.progress * 100 + "%";
      $("#anMsg").textContent = j.message;
    });
    await loadScore();
  } catch (e) { $("#anMsg").textContent = "erro: " + e.message; }
  finally {
    analyzing = false; drawMergeList();
    ["#btnAnalyze", "#source", "#btnReload"].forEach((id) => $(id).disabled = false);
  }
}

async function loadScore() {
  const d = await api(`/api/score?file=${encodeURIComponent(S.source)}`);
  S.score = d.score; S.candidates = d.candidates; S.duration = d.score.duration;
  $("#secTimeline").classList.remove("hidden");
  drawTimeline();
}

// ---------------------------------------------------------------- timeline
function drawTimeline() {
  const W = 1000, H = 180, sc = S.score;
  const n = sc.smooth.length, step = Math.max(1, Math.floor(n / W));
  let pts = "";
  for (let i = 0; i < n; i += step) {
    const x = (sc.times[i] / S.duration) * W;
    const y = H - 5 - sc.smooth[i] * (H - 20);
    pts += `${x.toFixed(1)},${y.toFixed(1)} `;
  }
  const thrY = H - 5 - sc.threshold * (H - 20);
  const cand = S.candidates
    .map((c) => `<line x1="${(c.t / S.duration) * W}" y1="${H}" x2="${(c.t / S.duration) * W}" y2="${H - 5 - c.score * (H - 20)}" stroke="#a7dfff" stroke-width="1.4" opacity=".55"/>`)
    .join("");
  const spans = S.shorts
    .map((s) => {
      const cd = cutSecs(s);
      const bars = s.cuts
        .map((c) => {
          const x = (c.start / S.duration) * W, ww = (cd / S.duration) * W;
          return `<rect x="${x}" y="4" width="${Math.max(ww, 0.6)}" height="${H - 8}" fill="${s.color}" opacity=".14"/>`;
        })
        .join("");
      const lx = (firstStart(s) / S.duration) * W;
      return `${bars}<text x="${lx + 4}" y="18" fill="${s.color}" font-size="11" opacity=".7">${s.name}</text>`;
    })
    .join("");
  $("#tl").innerHTML = `
    <rect width="${W}" height="${H}" fill="transparent"/>
    ${spans}
    <line x1="0" y1="${thrY}" x2="${W}" y2="${thrY}" stroke="#ff765d" stroke-dasharray="4 4" opacity=".6"/>
    <polyline points="${pts}" fill="none" stroke="#daff64" stroke-width="1.6"/>
    ${cand}`;
}
$("#tl")?.addEventListener("click", (ev) => {
  const r = ev.currentTarget.getBoundingClientRect();
  const t = ((ev.clientX - r.left) / r.width) * S.duration;
  $("#peek").src = `/api/frame?file=${encodeURIComponent(S.source)}&t=${t.toFixed(2)}&w=220`;
});

// ---------------------------------------------------------------- grouping
async function group() {
  if (!S.music) { $("#musicInfo").textContent = "confirme a batida da faixa antes de agrupar."; return; }
  S.entryBeats = +$("#entryBeats").value;
  const g = await post("/api/group", {
    file: S.source,
    batch_size: +$("#batchSize").value,
    cuts_per: +$("#cutsPer").value,
    music: S.music,
    entry_beats: S.entryBeats,
    spread: +$("#spread").value,
  });
  S.cutSeconds = g.cut_seconds;
  S.music = g.music;
  S.shorts = g.edits;
  $("#secShorts").classList.remove("hidden");
  $("#secRender").classList.remove("hidden");
  renderShorts();
  drawTimeline();
}

const shortBpm = (s) => +(s.music?.bpm || S.music?.bpm || BPM);
const cutSecs = (s) => (s._beats || s.cuts[0]?.beats || 8) * 60 / shortBpm(s);
const firstStart = (s) => Math.min(...s.cuts.map((c) => c.start));

function renderShorts() {
  const box = $("#shorts");
  box.innerHTML = "";
  S.shorts.forEach((s, si) => {
    s._beats = s._beats || s.cuts[0]?.beats || 8;
    const dur = s.cuts.length * cutSecs(s);
    const ok = dur >= 19.99 && dur <= 22.01;
    const el = document.createElement("div");
    el.className = "short";
    el.innerHTML = `
      <div class="head">
        <img src="/api/frame?file=${encodeURIComponent(S.source)}&t=${(s._peak).toFixed(2)}&w=260" alt="">
        <div class="fields">
          <label>Nome <input type="text" data-f="name" value="${s.name}" size="20"></label>
          <label>Título <input type="text" data-f="title" value="${s.title}" size="22" placeholder="TEXTO DO SHORT"></label>
          <label>Tema/tag <input type="text" data-f="tag" value="${s.tag}" size="16" placeholder="CASA / PISTOLA"></label>
          <label>Cor <input type="text" data-f="color" value="${s.color}" size="8"></label>
          <label>Beats/corte <input type="number" data-f="_beats" value="${s._beats}" min="4" max="16" step="1"></label>
          <label>Faixa
            <select data-f="_music">
              <option value="">(padrão: ${S.music?.file || "—"})</option>
              ${S.musicReg.filter((m) => m.known).map((m) => `<option value="${m.file}" ${s.music?.file === m.file && s._musicOverride ? "selected" : ""}>${m.file}</option>`).join("")}
            </select>
          </label>
          <label>Entrada (beats)
            <select data-f="_entry">${[0, 4, 8, 12, 16].map((n) => `<option ${(+s._entry_beats || 0) === n ? "selected" : ""}>${n}</option>`).join("")}</select>
          </label>
          <span class="muted">música em ${(+s.music_start).toFixed(2)}s</span>
          <span class="dur ${ok ? "ok" : "bad"}">${dur.toFixed(2)} s</span>
          <button class="ghost" data-act="del">remover short</button>
        </div>
      </div>
      <div class="cuts"></div>
      <button class="ghost" data-act="addcut">＋ corte</button>`;
    const cutsBox = $(".cuts", el);
    s.cuts.forEach((c, ci) => {
      const row = document.createElement("div");
      row.className = "cut";
      row.innerHTML = `
        <span class="n">${ci + 1}</span>
        <button class="ghost" data-act="nudge" data-d="-0.5">−</button>
        <input type="number" step="0.1" data-c="start" value="${(+c.start).toFixed(1)}">
        <button class="ghost" data-act="nudge" data-d="0.5">＋</button>
        <label><input type="checkbox" data-c="replay" ${c.replay ? "checked" : ""}> replay</label>
        <button class="ghost" data-act="see">ver</button>
        <button class="ghost" data-act="rmcut">✕</button>`;
      row.querySelectorAll("[data-c]").forEach((inp) =>
        inp.addEventListener("change", () => {
          if (inp.dataset.c === "replay") c.replay = inp.checked;
          else c.start = parseFloat(inp.value) || 0;
          syncShort(si);
        }));
      row.querySelector('[data-act="nudge"]').parentNode
        .querySelectorAll('[data-act="nudge"]').forEach((b) =>
          b.addEventListener("click", () => { c.start = Math.max(0, +(c.start + parseFloat(b.dataset.d)).toFixed(2)); syncShort(si); }));
      row.querySelector('[data-act="see"]').addEventListener("click", () => {
        $("img", el).src = `/api/frame?file=${encodeURIComponent(S.source)}&t=${(+c.start + 1).toFixed(2)}&w=260`;
      });
      row.querySelector('[data-act="rmcut"]').addEventListener("click", () => { s.cuts.splice(ci, 1); syncShort(si); });
      cutsBox.appendChild(row);
    });
    el.querySelectorAll("[data-f]").forEach((inp) =>
      inp.addEventListener("change", () => {
        const f = inp.dataset.f;
        if (f === "_beats") { s._beats = +inp.value; s.cuts.forEach((c) => (c.beats = +inp.value)); }
        else if (f === "name") s.name = inp.value.toUpperCase().replace(/[^A-Z0-9_]/g, "_");
        else if (f === "_entry") {
          s._entry_beats = +inp.value;
          const t = s._musicOverride ? { ...s.music, duration: regEntry(s.music.file)?.duration } : S.music;
          s.music_start = musicStart(t, s._entry_beats);
        } else if (f === "_music") {
          if (inp.value) {
            const m = regEntry(inp.value);
            s.music = { file: m.file, sha256: m.sha256, bpm: m.bpm,
              grid_offset_seconds: m.grid_offset_seconds, evidence: m.evidence };
            s._musicOverride = true;
            s.music_start = musicStart({ ...m }, +s._entry_beats || 0);
          } else {
            s._musicOverride = false;
            s.music = { file: S.music.file, sha256: S.music.sha256, bpm: S.music.bpm,
              grid_offset_seconds: S.music.grid_offset_seconds, evidence: S.music.evidence };
            s.music_start = musicStart(S.music, +s._entry_beats || 0);
          }
        } else s[f] = inp.value;
        syncShort(si);
      }));
    el.querySelector('[data-act="del"]').addEventListener("click", () => { S.shorts.splice(si, 1); renderShorts(); drawTimeline(); });
    el.querySelector('[data-act="addcut"]').addEventListener("click", () => {
      const last = s.cuts[s.cuts.length - 1];
      s.cuts.push({ ...structuredClone(last || { center_x: .5, gamma: 1.1, speed: 1, replay: false }),
        start: +(((last?.start) || 0) + cutSecs(s)).toFixed(2),
        beats: s._beats, note: "corte adicional (manual)." });
      syncShort(si);
    });
    box.appendChild(el);
  });
}
function syncShort() { renderShorts(); drawTimeline(); }

$("#btnAddShort")?.addEventListener("click", () => {});

// ---------------------------------------------------------------- plan + render
async function makePlan() {
  for (const s of S.shorts) {
    s.cuts.forEach((c) => { c.beats = s._beats; delete c._x; });
    if (!s.title.trim() || !s.tag.trim()) { $("#planMsg").textContent = `preencha título e tema de ${s.name}`; return; }
  }
  const clean = S.shorts.map((s) => {
    const { _beats, _peak, _score, _entry_beats, _musicOverride, ...rest } = s;
    return rest;
  });
  try {
    const r = await post("/api/plan", { file: S.source, edits: clean, music: S.music });
    S.planPath = r.plan_path;
    $("#planMsg").textContent = (r.ok ? "✓ plano válido — " : "✗ ") + r.message;
    $("#planMsg").className = r.ok ? "pill ok" : "pill bad";
    $("#btnRender").disabled = !r.ok;
  } catch (e) { $("#planMsg").textContent = "erro: " + e.message; }
}

async function render() {
  $("#btnRender").disabled = true;
  const bar = $("#rndBar"); bar.classList.remove("hidden");
  const log = $("#log"); log.classList.remove("hidden");
  try {
    const { job } = await post("/api/render", { plan_path: S.planPath });
    const j = await pollJob(job, (jj) => {
      bar.querySelector("i").style.width = jj.progress * 100 + "%";
      $("#rndMsg").textContent = jj.message;
      log.textContent = jj.log.slice(-40).join("\n");
      log.scrollTop = log.scrollHeight;
    });
    await loadReview(j.result.output);
  } catch (e) { $("#rndMsg").textContent = "erro: " + e.message; $("#btnRender").disabled = false; }
}

async function loadReview(output) {
  const b = await api(`/api/batch/${output}`);
  $("#secReview").classList.remove("hidden");
  if (b.watch) $("#watchLink").href = b.watch;
  $("#review").innerHTML = b.items.map((it) => `
    <article>
      ${it.video ? `<video controls playsinline preload="none" poster="${it.poster || ""}" src="${it.video}"></video>` : `<div style="aspect-ratio:9/16;display:grid;place-items:center" class="muted">não renderizado</div>`}
      <div class="meta">
        <strong>${it.name}</strong><br>
        <span class="muted">${it.title} · ${it.tag}</span><br>
        <span class="muted">${it.loudness != null ? it.loudness.toFixed(1) + " LUFS" : ""}</span>
      </div>
    </article>`).join("");
}

// ---------------------------------------------------------------- wiring
$("#btnTrain").addEventListener("click", async () => {
  const bar = $("#trainBar"), msg = $("#trainMsg");
  $("#btnTrain").disabled = true;
  bar.classList.remove("hidden");
  $("#modelPill").textContent = "treinando…"; $("#modelPill").className = "pill";
  try {
    const { job } = await post("/api/train", { raw_only: $("#trainRawOnly").checked });
    await pollJob(job, (j) => {
      bar.querySelector("i").style.width = j.progress * 100 + "%";
      msg.textContent = `${(j.progress * 100) | 0}% · ${j.message}`;
    });
    msg.textContent = "modelo atualizado.";
    await loadModel();
  } catch (e) {
    msg.textContent = "erro: " + e.message;
    $("#modelPill").textContent = "erro no treino"; $("#modelPill").className = "pill bad";
  } finally {
    $("#btnTrain").disabled = false;
    setTimeout(() => bar.classList.add("hidden"), 1500);
  }
});
$("#btnReload").addEventListener("click", loadSources);
$("#btnMergeAdd").addEventListener("click", () => {
  const file = $("#mergeSource").value;
  if (file && !mergeFiles.includes(file)) mergeFiles.push(file);
  drawMergeList();
});
$("#btnMerge").addEventListener("click", mergeVideos);
$("#source").addEventListener("change", onSourcePick);
$("#btnAnalyze").addEventListener("click", analyze);
$("#musicFile").addEventListener("change", onMusicPick);
$("#btnBeat").addEventListener("click", analyzeBeat);
$("#entryBeats").addEventListener("change", () => (S.entryBeats = +$("#entryBeats").value));
$("#btnGroup").addEventListener("click", group);
$("#btnPlan").addEventListener("click", makePlan);
$("#btnRender").addEventListener("click", render);

loadModel();
loadSources();
loadMusic();
