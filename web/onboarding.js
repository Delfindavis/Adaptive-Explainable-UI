// Member 2: learner context, diagnostic questions, and validation in the browser.
export function onboarding(host, onSubmit) {
  host.innerHTML = `
    <div class="eyebrow">01 / GET STARTED</div>
    <h1>A learning space that fits you.</h1>
    <p class="lead">Tell us a little about yourself, then try three short questions.</p>
    <form id="profile-form" class="card">
      <div class="form-grid">
        <label>Experience with Python<select name="experience_level"><option value="beginner">Beginner</option><option value="intermediate">Intermediate</option><option value="advanced">Advanced</option></select></label>
        <label>How would you like to learn?<select name="learning_preference"><option value="example">Worked examples</option><option value="hint">Step-by-step hints</option><option value="concise">Short explanations</option><option value="challenge">A challenge first</option></select></label>
        <label>Device you are using<select name="device_type"><option value="desktop">Desktop / laptop</option><option value="mobile">Mobile</option><option value="tablet">Tablet</option></select></label>
      </div>
      <h2>A quick starting point</h2><p>It is fine to choose “I don’t know”. This is a diagnostic, not a grade.</p>
      ${question('q0', '1. Which symbol checks equality in Python?', ['=', '==', '!=', 'I don’t know'])}
      ${question('q1', '2. Is 7 > 4 true or false?', ['True', 'False', 'I don’t know'])}
      ${question('q2', '3. When does an else block run?', ['When the if condition is true', 'When the if condition is false', 'On every run', 'I don’t know'])}
      <p id="form-error" class="error" role="alert"></p><button type="submit">Open my lesson <span>→</span></button>
    </form>`;
  host.querySelector('form').addEventListener('submit', async event => {
    event.preventDefault();
    const form = event.currentTarget;
    const data = new FormData(form);
    const button = form.querySelector('button');
    button.disabled = true;
    try {
      await onSubmit({experience_level: data.get('experience_level'), learning_preference: data.get('learning_preference'), device_type: data.get('device_type'), answers: ['q0','q1','q2'].map(k => Number(data.get(k)))});
    } catch (error) {
      form.querySelector('#form-error').textContent = error.message;
      button.disabled = false;
    }
  });
}

export function question(name, title, choices) {
  return `<fieldset><legend>${title}</legend>${choices.map((choice, index) => `<label class="choice"><input type="radio" name="${name}" value="${index}" required> <span>${choice}</span></label>`).join('')}</fieldset>`;
}
