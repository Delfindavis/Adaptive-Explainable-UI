// Member 3: the same objective and assessment in four presentation styles.
import { question } from './onboarding.js';
export const names = {hint:'Hint-heavy', example:'Example-driven', concise:'Concise', challenge:'Challenge-oriented'};
const code = `temperature = 32\nif temperature > 30:\n    print("Hot day")\nelse:\n    print("Mild day")`;
const core = `<p><strong>if</strong> checks a condition. Its indented block runs when the condition is true. <strong>else</strong> runs when it is false. Put a colon after each branch header and indent its statements consistently. Use <code>==</code> for equality, <code>&gt;</code> for greater than, and <code>&gt;=</code> for greater than or equal to.</p>`;
const views = {
  hint: `<h2>Take it one step at a time</h2>${core}<ol class="steps"><li>Read the value: <code>temperature = 32</code>.</li><li>Check the condition: is 32 greater than 30?</li><li>Yes. Run the indented <code>if</code> block.</li><li>Skip the <code>else</code> block. The output is <strong>Hot day</strong>.</li></ol><pre><code>${code}</code></pre><details><summary>Hint: what if the temperature is exactly 30?</summary><p>The condition uses <code>&gt;</code>, not <code>&gt;=</code>. At 30 it is false, so the output is “Mild day”.</p></details>`,
  example: `<h2>See the rule in action</h2>${core}<pre><code>${code}</code></pre><div class="table-wrap"><table><thead><tr><th>Temperature</th><th>Greater than 30?</th><th>Output</th></tr></thead><tbody><tr><td>32</td><td>True</td><td>Hot day</td></tr><tr><td>24</td><td>False</td><td>Mild day</td></tr><tr><td>30</td><td>False</td><td>Mild day</td></tr></tbody></table></div><p>Only one branch runs. At the boundary, 30 is not greater than 30.</p>`,
  concise: `<h2>The essentials</h2>${core}<pre><code>${code}</code></pre><p><strong>32 → Hot day.</strong> Values of 30 or below → Mild day.</p><p>Use <code>==</code> to compare equality; <code>=</code> assigns a value.</p>`,
  challenge: `<h2>Predict, then check</h2><p>What will this program print? What changes when <code>temperature</code> becomes 30?</p><pre><code>${code}</code></pre><details><summary>Reveal the worked answer</summary><p>At 32: <strong>Hot day</strong>. At 30: <strong>Mild day</strong>, because 30 &gt; 30 is false.</p></details>${core}`
};

export function lesson(host, session, onVariant, onComplete) {
  host.innerHTML = `<div class="eyebrow">02 / YOUR LESSON</div><h1>Make a decision with Python.</h1><p class="lead">Learn to trace a simple <code>if / else</code> statement.</p>
    <div class="notice"><strong>Phase I selection: fixed demo rule</strong><p id="reason"></p><small>This prototype does not train a bandit or generate SHAP/LIME explanations.</small></div>
    <div class="toolbar"><span>Presentation style</span><select id="style-select" aria-label="Presentation style">${Object.entries(names).map(([key,value]) => `<option value="${key}">${value}</option>`).join('')}</select><span class="muted">Switch styles for the review demo.</span></div>
    <article class="card" id="lesson-content"></article><p class="error" role="alert" id="lesson-error"></p>
    <form class="card" id="assessment"><div class="eyebrow">03 / CHECK YOUR UNDERSTANDING</div><h2>Try it yourself</h2><p>The same assessment is used for every presentation style.</p>
    ${question('a0', '1. If temperature = 29, what does the lesson program print?', ['Hot day', 'Mild day', 'Both messages'])}
    ${question('a1', '2. Which condition means “score is at least 50”?', ['score > 50', 'score >= 50', 'score == 50'])}
    ${question('a2', '3. If x = 5, what does “if x == 5: print(\'Yes\')” print?', ['Nothing', 'Yes', '5'])}
    <button type="submit">Finish lesson →</button></form>`;
  const select = host.querySelector('#style-select');
  const reason = host.querySelector('#reason');
  const render = () => {
    select.value = session.ui_variant;
    reason.textContent = session.reason;
    host.querySelector('#lesson-content').innerHTML = views[session.ui_variant];
  };
  render();
  select.addEventListener('change', async () => {
    select.disabled = true;
    host.querySelector('#assessment button').disabled = true;
    try {session = await onVariant(select.value); render();}
    catch (error) {host.querySelector('#lesson-error').textContent = error.message; render();}
    finally {select.disabled = false; host.querySelector('#assessment button').disabled = false;}
  });
  host.querySelector('#assessment').addEventListener('submit', async event => {
    event.preventDefault();
    const button = event.currentTarget.querySelector('button');
    const data = new FormData(event.currentTarget);
    button.disabled = true;
    select.disabled = true;
    try {await onComplete(['a0','a1','a2'].map(k => Number(data.get(k))));}
    catch(error) {host.querySelector('#lesson-error').textContent = error.message; button.disabled = false; select.disabled = false;}
  });
}
