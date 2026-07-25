const DATA = __DATA__;
const COLORS = ["var(--p0)","var(--p1)","var(--p2)","var(--p3)"];
const state = {phase:0, q:"", missing:false, index:false};

const esc = s => String(s).replace(/[&<>"]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const hl = (s,q) => q ? esc(s).replace(new RegExp("("+q.replace(/[.*+?^${}()|[\]\\]/g,"\\$&")+")","ig"),"<mark>$1</mark>") : esc(s);
const match = (ex,q) => !q || (ex.name+" "+ex.notes).toLowerCase().includes(q.toLowerCase());

/* --- Jahresleiste --- */
function renderYear(){
  const weeks = DATA.phases.map(p => p.weeks || 4);
  document.getElementById("totalweeks").textContent =
    DATA.phases.reduce((a,p)=>a+(p.weeks||0),0) + " Wochen verplant";
  document.getElementById("year").innerHTML = DATA.phases.map((p,i)=>`
    <button class="seg" style="--w:${weeks[i]};--c:${COLORS[i%4]}"
            aria-pressed="${!state.index && state.phase===i}" data-phase="${i}">
      <span class="bar"></span>
      <span class="lab">${esc(p.name)}</span>
      <span class="wk">${p.weeks ? p.weeks+" Wochen" : "eingestreut"}</span>
    </button>`).join("");
  document.querySelectorAll(".seg").forEach(b =>
    b.onclick = () => { state.phase = +b.dataset.phase; state.index = false; renderShell(); });
}

/* --- Phasenansicht --- */
function phaseHead(p){
  const sets = p.routines.reduce((a,r)=>a+r.sets,0);
  const mins = p.routines.reduce((a,r)=>a+r.minutes,0);
  return `<div class="phase-head">
      <h2>${esc(p.name)}</h2>
      <div class="focus">${esc(p.focus)}${p.span?" · "+esc(p.span):""}</div>
      <div class="stats">
        <div class="stat"><b>${p.routines.length}</b><span>Routinen</span></div>
        <div class="stat"><b>${sets}</b><span>Sätze</span></div>
        <div class="stat"><b>${(mins/60).toFixed(1)} h</b><span>pro Durchgang</span></div>
      </div>
    </div>`;
}

function phaseResults(){
  const p = DATA.phases[state.phase], q = state.q, only = state.missing;
  let hits = 0;
  const cards = p.routines.map(r => {
    const rows = r.exercises.filter(e => match(e,q) && (!only || !e.numbers));
    hits += rows.length;
    const body = rows.length ? rows.map(e => `
      <div class="ex${e.group?" ss":""}">
        <span class="pos">${e.group?`<b>${e.group}</b>`:""}${e.pos}</span>
        <span class="name">${hl(e.name,q)}</span>
        <span class="set${e.numbers?"":" est"}">${esc(e.summary)}</span>
        ${e.notes?`<span class="note">${hl(e.notes,q)}</span>`:""}
      </div>`).join("")
      : `<div class="empty">Keine Übung passt zum Filter.</div>`;
    return `<article class="routine">
      <header>
        <h3>${esc(r.title)}</h3>
        <div class="meta">${r.exercises.length} Übungen · ${r.sets} Sätze · ca. ${r.minutes} min · Ø ${r.rest}s Pause</div>
        <div class="load">${r.exercises.map(e=>`<i style="flex:${e.sets}"></i>`).join("")}</div>
      </header>${body}</article>`;
  }).join("");
  return {html:`<div class="grid">${cards}</div>`, hits};
}

/* --- Übungs-Index über alle Phasen --- */
function indexHead(){
  const n = new Set();
  DATA.phases.forEach(p=>p.routines.forEach(r=>r.exercises.forEach(e=>n.add(e.name))));
  return `<div class="phase-head">
      <h2 style="color:var(--ink)">Übungs-Index</h2>
      <div class="focus">Welche Übung läuft durch wie viele Phasen — sortiert nach Wiederkehr</div>
      <div class="stats"><div class="stat"><b>${n.size}</b><span>Übungen gesamt</span></div></div>
    </div>`;
}

function indexResults(){
  const map = new Map();
  DATA.phases.forEach((p,pi) => p.routines.forEach(r => r.exercises.forEach(e => {
    if(!map.has(e.name)) map.set(e.name,{name:e.name, phases:new Set(), sets:0, where:[]});
    const v = map.get(e.name); v.phases.add(pi); v.sets += e.sets;
    if(!v.where.includes(r.title)) v.where.push(r.title);
  })));
  const rows = [...map.values()]
    .filter(v => match({name:v.name, notes:v.where.join(" ")}, state.q))
    .sort((a,b) => b.phases.size-a.phases.size || b.sets-a.sets || a.name.localeCompare(b.name));

  return {hits:rows.length, html:`<table class="index-table">
      <thead><tr><th>Übung</th><th>Phasen</th><th>Routinen</th><th class="num">Sätze gesamt</th></tr></thead>
      <tbody>${rows.map(v => `<tr>
        <td>${hl(v.name,state.q)}</td>
        <td><span class="dots">${DATA.phases.map((p,i)=>
            `<i class="${v.phases.has(i)?"on":""}" style="--c:${COLORS[i%4]}" title="${esc(p.name)}"></i>`).join("")}</span></td>
        <td style="color:var(--muted);font-size:13px">${esc(v.where.join(", "))}</td>
        <td class="num">${v.sets}</td></tr>`).join("")}
      </tbody></table>`};
}

/* --- Rendern: Gerüst einmal, Ergebnisse bei jedem Tastendruck --- */
function renderResults(){
  const {html, hits} = state.index ? indexResults() : phaseResults();
  document.getElementById("results").innerHTML = html;
  document.getElementById("hits").textContent = hits + " Treffer";
}

function renderShell(){
  document.documentElement.style.setProperty("--accent", COLORS[state.phase%4]);
  renderYear();
  document.getElementById("main").innerHTML =
    (state.index ? indexHead() : phaseHead(DATA.phases[state.phase])) + `
    <div class="controls">
      <input type="search" id="q" placeholder="Übung oder Notiz suchen …" value="${esc(state.q)}">
      <button class="toggle" id="tMissing" aria-pressed="${state.missing}" ${state.index?"hidden":""}>Nur ohne Zahlen</button>
      <button class="toggle" id="tIndex" aria-pressed="${state.index}">Übungs-Index</button>
      <span class="hits" id="hits"></span>
    </div>
    <div id="results"></div>`;

  document.getElementById("q").oninput = e => { state.q = e.target.value; renderResults(); };
  document.getElementById("tIndex").onclick = () => { state.index = !state.index; renderShell(); };
  const m = document.getElementById("tMissing");
  if(m) m.onclick = () => { state.missing = !state.missing;
    m.setAttribute("aria-pressed", state.missing); renderResults(); };
  renderResults();
}

document.getElementById("stand").textContent =
  new Date().toLocaleDateString("de-DE",{day:"2-digit",month:"long",year:"numeric"});
renderShell();