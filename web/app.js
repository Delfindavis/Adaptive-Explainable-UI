// Member 4: navigation, API integration, dataset view and result presentation.
import { onboarding } from './onboarding.js';
import { lesson, names } from './lesson.js';
const host = document.querySelector('#app');
let session = null;
async function api(path, data) {
  const response = await fetch(path, data ? {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(data)} : {});
  const result = await response.json();
  if (!response.ok) throw new Error(result.error || 'Request failed');
  return result;
}
const remember = value => {session = value; sessionStorage.setItem('adaptlearn_session', value.session_id); return value;};
function setActive(tab) {
  document.querySelector('#learn-nav').classList.toggle('active', tab === 'learn');
  document.querySelector('#data-nav').classList.toggle('active', tab === 'data');
}
function showLearning() {
  setActive('learn');
  if (!session) return onboarding(host, async data => {remember(await api('/api/start', data)); showLearning();});
  if (session.result) return showResult();
  lesson(host, session,
    async variant => remember(await api('/api/variant', {session_id:session.session_id, ui_variant:variant})),
    async answers => {remember(await api('/api/complete', {session_id:session.session_id, answers})); showResult();});
}
function reset() {session = null; sessionStorage.removeItem('adaptlearn_session'); showLearning();}
function showResult() {
  const result = session.result;
  host.innerHTML = `<div class="eyebrow">LESSON COMPLETE</div><h1>A small step, recorded.</h1><p class="lead">Your result is saved locally. Phase II will connect this feedback to the learning algorithm.</p>
    <div class="metrics"><div class="metric"><strong>${result.correct} / 3</strong><span>Assessment correct</span></div><div class="metric"><strong>${result.reward.toFixed(2)}</strong><span>Demonstration reward</span></div><div class="metric"><strong>${names[session.ui_variant]}</strong><span>Final presentation style</span></div></div>
    <section class="card"><h2>Review the answers</h2><ol class="feedback">${[
      '29 is not greater than 30, so the program prints Mild day.',
      'score >= 50 includes 50 and every larger value.',
      'x == 5 is true when x is 5, so it prints Yes.'
    ].map((text, i) => `<li><strong class="${result.answers[i] === result.correct_answers[i] ? 'success' : 'error'}">${result.answers[i] === result.correct_answers[i] ? 'Correct' : 'Review'}</strong> — ${text}</li>`).join('')}</ol></section>
    <div class="notice"><strong>How the reward is calculated</strong><p>0.8 × quiz accuracy + 0.2 × completion. This is a proposed prototype formula, not a validated measure of learning.</p><small>${session.selection_method === 'manual_preview' ? 'You previewed UI styles during this session. This result is unsuitable for a controlled comparison of a single style.' : 'This session used a fixed selection rule.'} No model update has occurred.</small></div>
    <div class="actions"><button id="restart">Try another learner</button><a href="/api/download/interactions">Download local interaction records</a></div>`;
  document.querySelector('#restart').addEventListener('click', reset);
}
async function showData() {
  setActive('data');
  host.innerHTML = '<p>Loading synthetic dataset…</p>';
  try {
    const data = await api('/api/dataset');
    const columns = ['learner_id','diagnostic_score','learning_preference','ui_variant','quiz_correct','task_completed','reward'];
    host.innerHTML = `<div class="eyebrow">DATA EXPLORER / SYNTHETIC</div><h1>A reproducible starting point.</h1><p class="lead">Fictional learner contexts and simulated outcomes for testing the prototype.</p>
      <div class="metrics"><div class="metric"><strong>${data.count}</strong><span>Simulated events</span></div><div class="metric"><strong>4</strong><span>Available UI variants</span></div><div class="metric"><strong>${data.metadata.seed}</strong><span>Random seed</span></div></div>
      <section class="card"><h2>Randomly assigned interfaces</h2><p>Each event is assigned one UI uniformly at random; each UI has probability 0.25.</p>${Object.entries(data.ui_counts).map(([arm,count]) => `<div>${names[arm]} <strong>${count}</strong><div class="bar"><span style="width:${100*count/data.count}%"></span></div></div>`).join('')}</section>
      <section class="card"><h2>First 12 rows</h2><div class="table-wrap"><table><thead><tr>${columns.map(k => `<th>${k.replaceAll('_',' ')}</th>`).join('')}</tr></thead><tbody>${data.preview.map(row => `<tr>${columns.map(k => `<td>${escapeHtml(row[k])}</td>`).join('')}</tr>`).join('')}</tbody></table></div></section>
      <div class="notice"><strong>Simulation assumptions</strong><p>Diagnostic score, preference and UI choice influence sampled outcomes using hand-written rules. Initial engagement is unavailable. These rows do not prove that any UI improves real learning.</p></div><div class="actions"><a href="/api/download/synthetic">Download synthetic CSV</a><a href="/api/download/interactions">Download local interactions separately</a></div>`;
  } catch (error) {host.innerHTML = '<p class="error" role="alert"></p>'; host.firstChild.textContent = error.message;}
}
function escapeHtml(value) {return String(value).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));}
document.querySelector('#learn-nav').addEventListener('click', showLearning);
document.querySelector('#data-nav').addEventListener('click', showData);
const existing = sessionStorage.getItem('adaptlearn_session');
if (existing) {try {remember(await api('/api/session/' + encodeURIComponent(existing)));} catch {sessionStorage.removeItem('adaptlearn_session');}}
showLearning();
