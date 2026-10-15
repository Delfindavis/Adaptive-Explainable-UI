// Member 2: learner context, diagnostic questions, and validation in the browser.
export function onboarding(host, onSubmit) {
  host.innerHTML = `
    <section class="welcome-hero">
      <div class="hero-copy">
        <div class="hero-kicker">
          <span class="hero-kicker-dot"></span>
          PERSONALIZED LEARNING EXPERIENCE
        </div>

        <h1 class="hero-title">
          Learning that adapts
          <span class="gradient-text">to you.</span>
        </h1>

        <p class="hero-description">
          Explore Python through a learning interface tailored to your
          preferences. AdaptLearn uses learner context and a contextual
          bandit algorithm to explore different ways of presenting a lesson.
        </p>

        <div class="hero-pills">
          <span>✦ Adaptive interfaces</span>
          <span>⌘ Python fundamentals</span>
          <span>◈ Research prototype</span>
        </div>
      </div>

      <div class="hero-visual" aria-label="Four available learning styles">
        <div class="hero-orbit hero-orbit-one"></div>
        <div class="hero-orbit hero-orbit-two"></div>

        <div class="hero-center">
          <span class="hero-center-icon">✳</span>
          <strong>Learn your way</strong>
          <small>Four presentation styles</small>
        </div>

        <div class="floating-style floating-style-one">
          <span class="floating-icon">☷</span>
          <span>
            <strong>Step-by-step</strong>
            <small>Hints</small>
          </span>
        </div>

        <div class="floating-style floating-style-two">
          <span class="floating-icon">▤</span>
          <span>
            <strong>Worked examples</strong>
            <small>Learn by seeing</small>
          </span>
        </div>

        <div class="floating-style floating-style-three">
          <span class="floating-icon">↗</span>
          <span>
            <strong>Challenge first</strong>
            <small>Try it yourself</small>
          </span>
        </div>
      </div>
    </section>

    <section class="learning-overview">
      <div class="section-heading">
        <div>
          <div class="eyebrow">YOUR LEARNING JOURNEY</div>
          <h2>Start where you are.</h2>
          <p class="section-description">
            Share your preferences and answer three short questions
            to establish your starting point.
          </p>
        </div>

        <div class="journey-step">
          <span class="journey-step-number">01</span>
          <span>Getting started</span>
        </div>
      </div>

      <div class="style-grid">
        <article class="style-tile">
          <span class="style-icon style-icon-indigo">☷</span>
          <h3>Step-by-step hints</h3>
          <p>Break a concept into smaller, guided steps.</p>
        </article>

        <article class="style-tile">
          <span class="style-icon style-icon-violet">▤</span>
          <h3>Worked examples</h3>
          <p>Understand concepts through code and examples.</p>
        </article>

        <article class="style-tile">
          <span class="style-icon style-icon-cyan">⌁</span>
          <h3>Concise explanations</h3>
          <p>Focus on the essential rules and takeaways.</p>
        </article>

        <article class="style-tile">
          <span class="style-icon style-icon-amber">↗</span>
          <h3>Challenge first</h3>
          <p>Predict the result before revealing the explanation.</p>
        </article>
      </div>

      <div class="research-caption">
        <span class="research-caption-icon">✦</span>
        <p>
          <strong>Designed to explore adaptation.</strong>
          LinUCB selects a presentation style using learner context.
          This academic prototype does not claim that one style is
          universally better for learning.
        </p>
      </div>
    </section>

    <section class="onboarding-section">
      <div class="section-heading">
        <div>
          <div class="eyebrow">PERSONALIZE YOUR SESSION</div>
          <h2>Tell us how you learn.</h2>
          <p class="section-description">
            Your answers help establish the context for this session.
          </p>
        </div>
      </div>

      <form id="profile-form" class="card onboarding-form">
        <div class="form-section-heading">
          <span class="form-section-icon">01</span>
          <div>
            <h3>Your learning preferences</h3>
            <p>Choose the options that best describe you.</p>
          </div>
        </div>

        <div class="form-grid">
          <label>
            Experience with Python
            <select name="experience_level">
              <option value="beginner">Beginner</option>
              <option value="intermediate">Intermediate</option>
              <option value="advanced">Advanced</option>
            </select>
          </label>

          <label>
            How would you like to learn?
            <select name="learning_preference">
              <option value="example">Worked examples</option>
              <option value="hint">Step-by-step hints</option>
              <option value="concise">Short explanations</option>
              <option value="challenge">A challenge first</option>
            </select>
          </label>

          <label>
            Device you are using
            <select name="device_type">
              <option value="desktop">Desktop / laptop</option>
              <option value="mobile">Mobile</option>
              <option value="tablet">Tablet</option>
            </select>
          </label>
        </div>

        <div class="form-divider"></div>

        <div class="form-section-heading">
          <span class="form-section-icon">02</span>
          <div>
            <h3>Your starting point</h3>
            <p>
              Three quick questions help establish your Python baseline.
              Choosing “I don't know” is completely fine.
            </p>
          </div>
        </div>

        <div class="diagnostic-progress">
          <span>DIAGNOSTIC CHECK</span>
          <span>3 questions</span>
        </div>

        ${question(
          'q0',
          '1. Which symbol checks equality in Python?',
          ['=', '==', '!=', "I don't know"]
        )}

        ${question(
          'q1',
          '2. Is 7 > 4 true or false?',
          ['True', 'False', "I don't know"]
        )}

        ${question(
          'q2',
          '3. When does an else block run?',
          [
            'When the if condition is true',
            'When the if condition is false',
            'On every run',
            "I don't know"
          ]
        )}

        <div class="form-submit-area">
          <p class="form-reassurance">
            Your diagnostic is a starting point, not a grade.
          </p>

          <p id="form-error" class="error" role="alert"></p>

          <button type="submit" class="start-learning-button">
            Open my lesson <span aria-hidden="true">→</span>
          </button>
        </div>
      </form>
    </section>
  `;

  host.querySelector('form').addEventListener('submit', async event => {
    event.preventDefault();

    const form = event.currentTarget;
    const data = new FormData(form);
    const button = form.querySelector('button');

    button.disabled = true;

    try {
      await onSubmit({
        experience_level: data.get('experience_level'),
        learning_preference: data.get('learning_preference'),
        device_type: data.get('device_type'),
        answers: ['q0', 'q1', 'q2'].map(k =>
          Number(data.get(k))
        )
      });
    } catch (error) {
      form.querySelector('#form-error').textContent = error.message;
      button.disabled = false;
    }
  });
}

export function question(name, title, choices) {
  return `
    <fieldset class="diagnostic-question">
      <legend>${title}</legend>

      <div class="diagnostic-choices">
        ${choices.map((choice, index) => `
          <label class="choice">
            <input
              type="radio"
              name="${name}"
              value="${index}"
              required
            >
            <span>${choice}</span>
          </label>
        `).join('')}
      </div>
    </fieldset>
  `;
}