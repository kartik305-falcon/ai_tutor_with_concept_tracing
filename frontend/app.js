// ============================================================
// CodeTutor AI — Frontend v3.0
// Features: Socratic Mode, Smart Error Explainer, Image Debugger,
//           Study Notes + PDF, XP/Streak, JS Language, Code Duel,
//           Voice Input, GitHub Review, Learning Path
// ============================================================

const LANGUAGE_CONFIG = {
    "C": {
        icon: "⚙️",
        placeholder: "Ask me anything about C programming...",
        defaultCode: `#include <stdio.h>\n\nint main() {\n    int a, b;\n    scanf("%d %d", &a, &b);\n    printf("%d", a + b);\n    return 0;\n}`,
        defaultTests: "3 4 => 7\n10 20 => 30"
    },
    "Python": {
        icon: "🐍",
        placeholder: "Ask me anything about Python programming...",
        defaultCode: `a, b = map(int, input().split())\nprint(a + b)`,
        defaultTests: "3 4 => 7\n10 20 => 30"
    },
    "Java": {
        icon: "☕",
        placeholder: "Ask me anything about Java programming...",
        defaultCode: `import java.util.Scanner;\n\npublic class Main {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        int a = sc.nextInt();\n        int b = sc.nextInt();\n        System.out.print(a + b);\n    }\n}`,
        defaultTests: "3 4 => 7\n10 20 => 30"
    },
    "JavaScript": {
        icon: "🟨",
        placeholder: "Ask me anything about JavaScript...",
        defaultCode: `const lines = _readline().split(' ');\nconst a = parseInt(lines[0]);\nconst b = parseInt(lines[1]);\nconsole.log(a + b);`,
        defaultTests: "3 4 => 7\n10 20 => 30"
    }
};

const VIEW_META = {
    "chat":     { title: "💬 Tutor Chat",      sub: "Ask questions and get step-by-step explanations." },
    "practice": { title: "🧪 Code Practice",   sub: "Write, run, and grade your code against test cases." },
    "mastery":  { title: "📊 Concept Mastery", sub: "Track your progress and identify areas to improve." },
    "quiz":     { title: "🧠 Quiz",            sub: "Adaptive quiz generated from your weak concepts." },
    "debug":    { title: "🖼️ Error Debugger",  sub: "Upload a screenshot of your error. AI explains the concept behind it." },
    "duel":     { title: "⚔️ Code Duel",       sub: "Race the clock! Solve an AI challenge before time runs out." },
    "github":   { title: "🔗 GitHub Review",   sub: "Paste a public GitHub file URL for an AI code review." },
    "path":     { title: "🗺️ Learning Path",   sub: "Your personalized 7-day study plan based on your mastery data." }
};

// ── State ────────────────────────────────────────────────────
let currentLang = "C";
let currentView = "chat";
let chatHistories = { "C": [], "Python": [], "Java": [], "JavaScript": [] };
let quizData = null;
let socraticMode = false;
let currentNotes = null;
let duelDifficulty = "easy";
let duelTimerInterval = null;
let duelTimeLeft = 0;
let duelProblem = null;

// ── Markdown renderer (lightweight) ─────────────────────────
const simpleMD = (text) => {
    let out = text
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        .replace(/```(\w*)\n?([\s\S]*?)```/g, '<pre><code class="lang-$1">$2</code></pre>')
        .replace(/`([^`]+)`/g, '<code>$1</code>')
        .replace(/^### (.*$)/gm, '<h3>$1</h3>')
        .replace(/^## (.*$)/gm, '<h2>$1</h2>')
        .replace(/^> (.*$)/gm, '<blockquote>$1</blockquote>')
        .replace(/^- (.*$)/gm, '<li>$1</li>')
        .replace(/(<li>.*<\/li>)/gs, '<ul>$1</ul>')
        .replace(/\n/g, '<br>');
    return out;
};

// ── DOM ──────────────────────────────────────────────────────
const langPills      = document.querySelectorAll('.nav-pill');
const navItems       = document.querySelectorAll('.nav-item');
const views          = document.querySelectorAll('.view');
const pageTitle      = document.getElementById('page-title');
const pageSubtitle   = document.getElementById('page-subtitle');
const langBadge      = document.getElementById('current-lang-badge');
const chatHistoryDOM = document.getElementById('chat-history');
const chatInput      = document.getElementById('chat-input');
const chatSend       = document.getElementById('chat-send');
const fileUpload     = document.getElementById('file-upload');
const uploadStatus   = document.getElementById('upload-status');
const codeEditor     = document.getElementById('code-editor');
const testCasesArea  = document.getElementById('test-cases');
const runCodeBtn     = document.getElementById('run-code');
const genScenarioBtn = document.getElementById('gen-scenario');
const practiceResults = document.getElementById('practice-results');
const masteryDashboard = document.getElementById('mastery-dashboard');
const btnGenQuiz     = document.getElementById('generate-quiz');
const quizEmpty      = document.getElementById('quiz-empty-state');
const quizContent    = document.getElementById('quiz-content');
const socraticToggle = document.getElementById('socratic-toggle');
const socraticStatus = document.getElementById('socratic-status');
const notesBtnWrap   = document.getElementById('notes-btn-wrap');
const genNotesBtn    = document.getElementById('generate-notes-btn');
const notesPanel     = document.getElementById('notes-panel');
const notesContent   = document.getElementById('notes-content');
const exportPdfBtn   = document.getElementById('export-pdf-btn');
const closeNotesBtn  = document.getElementById('close-notes-btn');
const voiceBtn       = document.getElementById('voice-btn');

// ── Language Switcher ─────────────────────────────────────────
langPills.forEach(pill => {
    pill.addEventListener('click', (e) => {
        langPills.forEach(p => p.classList.remove('active'));
        e.currentTarget.classList.add('active');
        currentLang = e.currentTarget.getAttribute('data-lang');
        updateHeader();
        updateChatUI();
        updatePracticeUI();
    });
});

// ── View Switcher ─────────────────────────────────────────────
navItems.forEach(item => {
    item.addEventListener('click', (e) => {
        navItems.forEach(nav => nav.classList.remove('active'));
        e.currentTarget.classList.add('active');
        currentView = e.currentTarget.getAttribute('data-view');
        views.forEach(v => v.classList.remove('active'));
        document.getElementById(`view-${currentView}`).classList.add('active');
        updateHeader();

        // Show/hide per-view UI
        notesBtnWrap.style.display = currentView === 'chat' ? 'block' : 'none';
        document.getElementById('socratic-section').style.display = currentView === 'chat' ? 'block' : 'none';

        if (currentView === 'mastery') loadMastery();
    });
});

function updateHeader() {
    const meta = VIEW_META[currentView] || VIEW_META['chat'];
    pageTitle.innerHTML = `${meta.title} <span class="lang-badge" id="current-lang-badge">${currentLang}</span>`;
    pageSubtitle.innerText = meta.sub;
    langBadge.innerText = currentLang;
}

// ═══════════════════════════════ FEATURE 1: SOCRATIC MODE ═══
socraticToggle.addEventListener('click', () => {
    socraticMode = !socraticMode;
    socraticStatus.innerText = socraticMode ? 'ON' : 'OFF';
    socraticToggle.style.borderColor = socraticMode ? 'var(--accent-primary)' : '';
    socraticToggle.style.color = socraticMode ? 'var(--accent-primary)' : '';
});

// ═══════════════════════════════ CHAT LOGIC ══════════════════

function updateChatUI() {
    chatInput.placeholder = LANGUAGE_CONFIG[currentLang].placeholder;
    renderChatHistory();
    notesPanel.classList.add('hidden');
    currentNotes = null;
}

function renderChatHistory() {
    const history = chatHistories[currentLang];
    chatHistoryDOM.innerHTML = '';
    if (history.length === 0) {
        chatHistoryDOM.innerHTML = `<div class="empty-state"><div class="empty-icon">✦</div><div>Start by asking a question below</div></div>`;
        return;
    }
    history.forEach(msg => {
        const div = document.createElement('div');
        div.className = `chat-msg ${msg.role}`;
        div.innerHTML = msg.role === 'assistant' ? simpleMD(msg.content) : msg.content;
        chatHistoryDOM.appendChild(div);
    });
    chatHistoryDOM.scrollTop = chatHistoryDOM.scrollHeight;
}

chatSend.addEventListener('click', async () => {
    const text = chatInput.value.trim();
    if (!text) return;
    chatHistories[currentLang].push({ role: 'user', content: text });
    chatInput.value = '';
    renderChatHistory();

    const loader = document.createElement('div');
    loader.className = 'chat-msg assistant';
    loader.innerHTML = `<span style="color:var(--accent-primary)">${socraticMode ? '🎓 Thinking of a guiding question...' : 'Thinking...'}</span>`;
    chatHistoryDOM.appendChild(loader);
    chatHistoryDOM.scrollTop = chatHistoryDOM.scrollHeight;

    try {
        const historyPayload = chatHistories[currentLang].slice(0, -1).map(m => ({ role: m.role, content: m.content }));
        const res = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                message: text,
                history: historyPayload,
                language: currentLang.toLowerCase(),
                socratic_mode: socraticMode
            })
        });
        const data = await res.json();
        chatHistories[currentLang].push({ role: 'assistant', content: data.response });
    } catch (err) {
        chatHistories[currentLang].push({ role: 'assistant', content: `Error: ${err.message}` });
    }
    renderChatHistory();
    loadXP();
});

chatInput.addEventListener('keypress', (e) => { if (e.key === 'Enter') chatSend.click(); });

fileUpload.addEventListener('change', async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    uploadStatus.innerHTML = '<span style="color:var(--accent-primary)">Uploading...</span>';
    const formData = new FormData();
    formData.append('file', file);
    formData.append('language', currentLang.toLowerCase());
    try {
        const res = await fetch('/api/upload', { method: 'POST', body: formData });
        const data = await res.json();
        uploadStatus.innerText = res.ok ? data.message : `Failed: ${data.detail}`;
    } catch (err) {
        uploadStatus.innerHTML = `<span style="color:var(--error)">Error: ${err.message}</span>`;
    }
});

// ═══════════════════════════════ FEATURE 4: STUDY NOTES ══════

genNotesBtn.addEventListener('click', async () => {
    const history = chatHistories[currentLang];
    if (history.length < 2) {
        alert("Have at least one conversation before generating notes.");
        return;
    }
    genNotesBtn.innerText = 'Generating...';
    genNotesBtn.disabled = true;
    notesPanel.classList.remove('hidden');
    notesContent.innerHTML = '<div style="color:var(--accent-primary)">📝 Generating study notes...</div>';

    try {
        const payload = { history: history.map(m => ({ role: m.role, content: m.content })), language: currentLang.toLowerCase() };
        const res = await fetch('/api/study-notes', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
        const notes = await res.json();
        if (!res.ok || notes.error) throw new Error(notes.error || notes.detail);
        currentNotes = payload;
        renderNotes(notes);
    } catch (err) {
        notesContent.innerHTML = `<span style="color:var(--error)">Failed: ${err.message}</span>`;
    }
    genNotesBtn.innerText = '📝 Generate Notes';
    genNotesBtn.disabled = false;
});

function renderNotes(notes) {
    let ht = `<div style="font-size:1.1rem;font-weight:600;margin-bottom:1rem;color:var(--text-primary)">${notes.title || 'Study Notes'}</div>`;
    if (notes.summary) ht += `<p style="color:var(--text-secondary);margin-bottom:1rem;line-height:1.6">${notes.summary}</p>`;
    if (notes.key_concepts?.length) {
        ht += `<div style="margin-bottom:1rem;"><div style="font-weight:600;color:var(--accent-primary);margin-bottom:0.4rem;">🔑 Key Concepts</div><ul style="margin:0;padding-left:1.2rem;">`;
        notes.key_concepts.forEach(c => { ht += `<li style="color:var(--text-secondary);margin-bottom:0.2rem">${c}</li>`; });
        ht += `</ul></div>`;
    }
    if (notes.common_mistakes?.length) {
        ht += `<div style="margin-bottom:1rem;"><div style="font-weight:600;color:var(--warning);margin-bottom:0.4rem;">⚠️ Common Mistakes</div>`;
        notes.common_mistakes.forEach(m => { ht += `<div style="color:var(--text-secondary);font-size:0.9rem;margin-bottom:0.3rem">✗ ${m}</div>`; });
        ht += `</div>`;
    }
    if (notes.mini_quiz?.length) {
        ht += `<div><div style="font-weight:600;color:var(--success);margin-bottom:0.6rem;">🧠 Mini Quiz</div>`;
        notes.mini_quiz.forEach((q, i) => {
            ht += `<div style="margin-bottom:0.8rem;"><div style="font-weight:500;margin-bottom:0.2rem">Q${i+1}. ${q.question}</div>
                   <div style="color:var(--success);font-size:0.88rem">→ ${q.answer}</div></div>`;
        });
        ht += `</div>`;
    }
    notesContent.innerHTML = ht;
}

exportPdfBtn.addEventListener('click', async () => {
    if (!currentNotes) return;
    exportPdfBtn.innerText = 'Generating PDF...';
    exportPdfBtn.disabled = true;
    try {
        const res = await fetch('/api/study-notes/pdf', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(currentNotes)
        });
        if (!res.ok) throw new Error('PDF generation failed');
        const blob = await res.blob();
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'study_notes.pdf';
        a.click();
        URL.revokeObjectURL(url);
    } catch (err) {
        alert('PDF export failed: ' + err.message);
    }
    exportPdfBtn.innerText = '⬇️ Export PDF';
    exportPdfBtn.disabled = false;
});

closeNotesBtn.addEventListener('click', () => { notesPanel.classList.add('hidden'); });

// ═══════════════════════════════ FEATURE 8: VOICE INPUT ══════

let recognition = null;
if ('SpeechRecognition' in window || 'webkitSpeechRecognition' in window) {
    const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
    recognition = new SR();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = 'en-US';
    recognition.onresult = (e) => {
        chatInput.value = e.results[0][0].transcript;
        voiceBtn.style.color = '';
        voiceBtn.title = 'Voice Input (Chrome/Edge only)';
    };
    recognition.onerror = () => { voiceBtn.style.color = ''; };
    recognition.onend   = () => { voiceBtn.style.color = ''; };
} else {
    voiceBtn.title = 'Voice input not supported in this browser (use Chrome/Edge)';
    voiceBtn.style.opacity = '0.4';
}

voiceBtn.addEventListener('click', () => {
    if (!recognition) { alert('Voice input requires Chrome or Edge browser.'); return; }
    voiceBtn.style.color = '#e74c3c';
    recognition.start();
});

// ═══════════════════════════════ PRACTICE LOGIC ══════════════

function updatePracticeUI() {
    const cfg = LANGUAGE_CONFIG[currentLang];
    codeEditor.value = cfg.defaultCode;
    testCasesArea.value = cfg.defaultTests;
    practiceResults.classList.add('hidden');
}
updatePracticeUI();

genScenarioBtn.addEventListener('click', async () => {
    genScenarioBtn.innerHTML = 'Generating...';
    genScenarioBtn.disabled = true;
    try {
        const res = await fetch(`/api/scenario?language=${currentLang}&difficulty=medium`);
        if (!res.ok) throw new Error("Backend error");
        const data = await res.json();
        codeEditor.value = `/*\n  AI Challenge:\n  ${data.description}\n*/\n\n${data.default_code}`;
        testCasesArea.value = data.test_cases;
        practiceResults.innerHTML = `<div style="color:var(--success); padding: 1rem; text-align: center;">✅ Challenge loaded! Read the comment above for instructions.</div>`;
        practiceResults.classList.remove('hidden');
    } catch (err) { alert("Failed to generate scenario: " + err.message); }
    genScenarioBtn.innerHTML = '✨ AI Challenge';
    genScenarioBtn.disabled = false;
});

runCodeBtn.addEventListener('click', async () => {
    const code = codeEditor.value;
    const test_cases = parseTestCases(testCasesArea.value);
    if (test_cases.length === 0) { alert("No valid test cases. Format: input => expected"); return; }
    runCodeBtn.innerHTML = 'Running...';
    runCodeBtn.disabled = true;
    practiceResults.classList.add('hidden');
    try {
        const res = await fetch('/api/grade', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ code, test_cases, language: currentLang.toLowerCase() })
        });
        const data = await res.json();
        renderPracticeResults(data);
        loadXP();
    } catch (err) { alert("Error: " + err.message); }
    runCodeBtn.innerHTML = '▶ Run & Grade';
    runCodeBtn.disabled = false;
});

function parseTestCases(raw) {
    return raw.trim().split('\n')
        .filter(l => l.includes('=>'))
        .map(l => { const [inp, exp] = l.split('=>'); return { input: inp.trim(), expected: exp.trim() }; });
}

// ═══════════════════════════════ FEATURE 2: SMART ERROR EXPLAINER ═══
function renderPracticeResults(r) {
    let ht = `<div class="metrics-grid">
        <div class="metric-card"><div class="metric-label">Score</div><div class="metric-value">${(r.score * 100).toFixed(0)}%</div></div>
        <div class="metric-card"><div class="metric-label">Passed</div><div class="metric-value">${r.passed}</div></div>
        <div class="metric-card"><div class="metric-label">Total</div><div class="metric-value">${r.total}</div></div>
    </div><div>`;

    r.details.forEach(item => {
        if (item.status === 'passed') {
            ht += `<div class="test-result test-passed">✓ Test ${item.test} passed</div>`;
        } else {
            const safeStr = (s) => (s || '').replace(/"/g, '&quot;').replace(/'/g, '&#39;');
            const fnArgs = `${item.test}, '${safeStr(item.error || item.got)}', '${safeStr(item.expected)}', '${safeStr(item.input)}'`;
            ht += `<div class="test-result test-failed">
                ✗ Test ${item.test} failed
                <div class="test-detail">
                    ${item.error ? `<span>Error: ${item.error}</span>` : `<span><b>Expected:</b> ${item.expected}</span><span><b>Got:</b> ${item.got}</span>`}
                </div>`;

            // Smart Error Explainer card
            if (item.plain_explanation) {
                ht += `<div style="margin-top:0.5rem;padding:0.5rem 0.75rem;background:rgba(230,180,60,0.08);border-left:3px solid var(--warning);border-radius:4px;font-size:0.88rem;">
                    <span style="color:var(--warning);font-weight:600;">🔍 What this means: </span>${item.plain_explanation}
                </div>`;
            }

            ht += `<button class="btn-primary mt-2" style="padding:0.3rem 0.8rem;font-size:0.85rem;" onclick="window.fetchHint(${fnArgs})">✨ Get AI Hint</button>
                   <div id="hint-text-${item.test}" class="hidden" style="margin-top:0.5rem;padding:0.5rem;background:rgba(99,102,241,0.1);border-left:3px solid var(--accent-primary);font-size:0.9rem;"></div>
                   </div>`;
        }
    });

    ht += '</div>';
    if (r.pro_tip) {
        ht += `<div class="glass-panel mt-4" style="border:1px solid var(--success);">
            <div style="color:var(--success);font-weight:600;margin-bottom:0.5rem">💡 AI Pro Tip</div>
            <div style="font-size:0.95rem;line-height:1.5">${simpleMD(r.pro_tip)}</div>
        </div>`;
    }
    practiceResults.innerHTML = ht;
    practiceResults.classList.remove('hidden');
}

window.fetchHint = async function(testId, errorOrGot, expected, input) {
    const hintBox = document.getElementById(`hint-text-${testId}`);
    hintBox.innerHTML = '<span style="color:var(--accent-primary)">Generating hint...</span>';
    hintBox.classList.remove('hidden');
    try {
        const res = await fetch('/api/hint', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ code: codeEditor.value, test_input: input, test_expected: expected, error_or_got: errorOrGot, language: currentLang.toLowerCase() })
        });
        const data = await res.json();
        hintBox.innerHTML = data.hint.replace(/`([^`]+)`/g, '<code style="background:var(--bg-base);padding:0.1rem 0.3rem;border-radius:3px">$1</code>');
    } catch (err) {
        hintBox.innerHTML = `<span style="color:var(--error)">Failed: ${err.message}</span>`;
    }
};

// ═══════════════════════════════ MASTERY ═════════════════════

async function loadMastery() {
    masteryDashboard.innerHTML = '<div style="text-align:center;padding:2rem;">Loading analytics...</div>';
    try {
        const res = await fetch('/api/mastery');
        const data = await res.json();
        const concepts = data.concepts;
        if (!concepts || concepts.length === 0) {
            masteryDashboard.innerHTML = `<div class="empty-state"><div class="empty-icon">📊</div><div>No data yet — start practising!</div></div>`;
            return;
        }
        const strong = concepts.filter(c => c.confidence >= 0.8);
        const weak   = concepts.filter(c => c.confidence < 0.5);
        masteryDashboard.innerHTML = `
            <div class="metrics-grid" style="margin-bottom:1.5rem">
                <div class="metric-card"><div class="metric-label">Tracked</div><div class="metric-value">${concepts.length}</div></div>
                <div class="metric-card"><div class="metric-label">Strong ≥80%</div><div class="metric-value" style="color:var(--success)">${strong.length}</div></div>
                <div class="metric-card"><div class="metric-label">Weak &lt;50%</div><div class="metric-value" style="color:var(--warning)">${weak.length}</div></div>
            </div>
            <div class="concept-lists">
                <div class="glass-panel concept-panel">
                    <div class="section-header">⚠ Weak Concepts</div>
                    ${weak.length ? weak.map(c => `<div class="concept-item weak"><span>${c.concept}</span><span>${(c.confidence*100).toFixed(0)}%</span></div>`).join('') : '<div style="color:var(--text-secondary)">None detected 🎉</div>'}
                </div>
                <div class="glass-panel concept-panel">
                    <div class="section-header">✦ Strong Concepts</div>
                    ${strong.length ? strong.map(c => `<div class="concept-item strong"><span>${c.concept}</span><span>${(c.confidence*100).toFixed(0)}%</span></div>`).join('') : '<div style="color:var(--text-secondary)">Keep practising!</div>'}
                </div>
            </div>
            <div class="glass-panel" style="margin-top:1.5rem;overflow:hidden;">
                <table><thead><tr><th>Concept</th><th>Attempts</th><th>Confidence</th></tr></thead>
                <tbody>${concepts.map(c => `<tr><td>${c.concept}</td><td>${c.attempts}</td><td>${(c.confidence*100).toFixed(0)}%</td></tr>`).join('')}</tbody></table>
            </div>`;
    } catch (err) {
        masteryDashboard.innerHTML = `<div style="color:var(--error)">Failed to load mastery data.</div>`;
    }
}

// ═══════════════════════════════ QUIZ ════════════════════════

btnGenQuiz.addEventListener('click', async () => {
    quizEmpty.classList.add('hidden');
    quizContent.innerHTML = '<div style="text-align:center;padding:2rem;color:var(--accent-primary)">Generating adaptive quiz...</div>';
    quizContent.classList.remove('hidden');
    try {
        const res = await fetch(`/api/quiz?language=${currentLang}`);
        const data = await res.json();
        quizData = data.quiz;
        renderQuiz(data.quiz, data.weak_concepts);
        loadXP();
    } catch (err) {
        quizContent.innerHTML = `<div style="color:var(--error)">Error generating quiz.</div>`;
        quizEmpty.classList.remove('hidden');
    }
});

function renderQuiz(quiz, weakConcepts) {
    let ht = '';
    if (weakConcepts?.length) {
        ht += `<div class="weak-concepts-alert">Focusing on: <b>${weakConcepts.join(', ')}</b></div>`;
    }
    quiz.forEach((q, i) => {
        ht += `<div class="quiz-question-block" data-index="${i}">
            <div class="q-num">Question ${i+1} of ${quiz.length}</div>
            <div class="q-text">${q.question}</div>
            <div class="q-options">
                ${q.options.map(opt => `<label class="quiz-option" data-q="${i}" data-opt="${opt}">${opt}</label>`).join('')}
            </div></div>`;
    });
    ht += `<button id="submit-quiz" class="btn-primary mt-4">Submit Quiz</button>`;
    quizContent.innerHTML = ht;
    document.querySelectorAll('.quiz-option').forEach(opt => {
        opt.addEventListener('click', function() {
            if (document.getElementById('submit-quiz').disabled) return;
            this.closest('.q-options').querySelectorAll('.quiz-option').forEach(o => o.classList.remove('selected'));
            this.classList.add('selected');
        });
    });
    document.getElementById('submit-quiz').addEventListener('click', submitQuiz);
}

function submitQuiz() {
    let score = 0;
    quizData.forEach((q, i) => {
        const block = document.querySelector(`.quiz-question-block[data-index="${i}"]`);
        const selected = block.querySelector('.quiz-option.selected');
        block.querySelectorAll('.quiz-option').forEach(opt => {
            if (opt.getAttribute('data-opt') === q.answer) opt.classList.add('correct');
        });
        if (selected) {
            if (selected.getAttribute('data-opt') === q.answer) score++;
            else selected.classList.add('incorrect');
        }
    });
    document.getElementById('submit-quiz').disabled = true;
    const pct = score / quizData.length;
    const div = document.createElement('div');
    div.className = 'metrics-grid mt-4';
    div.innerHTML = `
        <div class="metric-card"><div class="metric-label">Score</div><div class="metric-value">${score}/${quizData.length}</div></div>
        <div class="metric-card" style="grid-column:span 2;display:flex;align-items:center;justify-content:center;flex-direction:column;border-color:${pct>=0.5?'var(--success)':'var(--warning)'}">
            <div style="font-weight:600;font-size:1.2rem;color:${pct>=0.5?'var(--success)':'var(--warning)'}">${pct>=0.5?'Improving 🎉':'Keep going 💪'}</div>
            <button id="retry-quiz" class="btn-primary mt-4" style="padding:0.4rem 1rem;font-size:0.8rem">Generate Another</button>
        </div>`;
    quizContent.appendChild(div);
    document.getElementById('retry-quiz').addEventListener('click', () => btnGenQuiz.click());
}

// ═══════════════════════════════ FEATURE 3: IMAGE DEBUGGER ═══

const debugFileInput  = document.getElementById('debug-file-input');
const debugUploadZone = document.getElementById('debug-upload-zone');
const debugPreview    = document.getElementById('debug-upload-preview');
const debugAnalyzeBtn = document.getElementById('debug-analyze-btn');
const debugResults    = document.getElementById('debug-results');
let debugFile = null;

debugUploadZone.addEventListener('click', () => debugFileInput.click());
debugUploadZone.addEventListener('dragover', (e) => { e.preventDefault(); debugUploadZone.style.borderColor = 'var(--accent-primary)'; });
debugUploadZone.addEventListener('dragleave', () => { debugUploadZone.style.borderColor = ''; });
debugUploadZone.addEventListener('drop', (e) => {
    e.preventDefault();
    debugUploadZone.style.borderColor = '';
    const f = e.dataTransfer.files[0];
    if (f && f.type.startsWith('image/')) setDebugFile(f);
});

debugFileInput.addEventListener('change', (e) => {
    const f = e.target.files[0];
    if (f) setDebugFile(f);
});

function setDebugFile(f) {
    debugFile = f;
    debugAnalyzeBtn.disabled = false;
    const reader = new FileReader();
    reader.onload = (ev) => {
        debugPreview.innerHTML = `<img src="${ev.target.result}" alt="Screenshot" style="max-height:200px;max-width:100%;border-radius:8px;margin-bottom:0.5rem;"><div style="color:var(--text-secondary);font-size:0.85rem">${f.name}</div>`;
    };
    reader.readAsDataURL(f);
}

debugAnalyzeBtn.addEventListener('click', async () => {
    if (!debugFile) return;
    debugAnalyzeBtn.innerText = '🔍 Analyzing...';
    debugAnalyzeBtn.disabled = true;
    debugResults.classList.add('hidden');
    debugResults.innerHTML = '';

    const formData = new FormData();
    formData.append('file', debugFile);
    formData.append('language', currentLang.toLowerCase());

    try {
        const res = await fetch('/api/debug-image', { method: 'POST', body: formData });
        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || 'Analysis failed');
        renderDebugResults(data);
    } catch (err) {
        debugResults.innerHTML = `<div class="glass-panel" style="padding:1rem;color:var(--error)">❌ ${err.message}</div>`;
        debugResults.classList.remove('hidden');
    }
    debugAnalyzeBtn.innerText = '🔍 Analyze Error';
    debugAnalyzeBtn.disabled = false;
});

function renderDebugResults(d) {
    debugResults.innerHTML = `
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin-top:0.5rem;">
            <div class="glass-panel" style="padding:1.25rem;border-left:3px solid var(--error);">
                <div style="font-size:0.7rem;text-transform:uppercase;letter-spacing:0.08em;color:var(--text-secondary);margin-bottom:0.4rem">❌ Error Detected</div>
                <div style="font-size:0.95rem;line-height:1.5">${d.error_detected}</div>
            </div>
            <div class="glass-panel" style="padding:1.25rem;border-left:3px solid var(--accent-primary);">
                <div style="font-size:0.7rem;text-transform:uppercase;letter-spacing:0.08em;color:var(--text-secondary);margin-bottom:0.4rem">🎯 Related Concept</div>
                <div style="font-size:0.95rem;font-weight:600;color:var(--accent-primary)">${d.concept}</div>
            </div>
            <div class="glass-panel" style="padding:1.25rem;border-left:3px solid var(--warning);">
                <div style="font-size:0.7rem;text-transform:uppercase;letter-spacing:0.08em;color:var(--text-secondary);margin-bottom:0.4rem">🤔 Why It Happens</div>
                <div style="font-size:0.9rem;line-height:1.6">${d.why_it_happens}</div>
            </div>
            <div class="glass-panel" style="padding:1.25rem;border-left:3px solid var(--success);">
                <div style="font-size:0.7rem;text-transform:uppercase;letter-spacing:0.08em;color:var(--text-secondary);margin-bottom:0.4rem">✅ How to Avoid It</div>
                <div style="font-size:0.9rem;line-height:1.6">${d.how_to_avoid}</div>
            </div>
        </div>
        ${d.example_fix ? `<div class="glass-panel" style="padding:1.25rem;margin-top:1rem;">
            <div style="font-size:0.7rem;text-transform:uppercase;letter-spacing:0.08em;color:var(--text-secondary);margin-bottom:0.6rem">💻 Example Fix</div>
            <pre style="margin:0;background:var(--bg-base);padding:0.75rem;border-radius:6px;font-size:0.85rem"><code>${escapeHtml(d.example_fix)}</code></pre>
        </div>` : ''}`;
    debugResults.classList.remove('hidden');
}

// ═══════════════════════════════ FEATURE 7: CODE DUEL ════════

document.querySelectorAll('.diff-btn').forEach(btn => {
    btn.addEventListener('click', function() {
        document.querySelectorAll('.diff-btn').forEach(b => b.classList.remove('active'));
        this.classList.add('active');
        duelDifficulty = this.getAttribute('data-diff');
    });
});

document.getElementById('duel-start-btn').addEventListener('click', async () => {
    const btn = document.getElementById('duel-start-btn');
    btn.innerText = 'Loading challenge...';
    btn.disabled = true;
    try {
        const res = await fetch(`/api/scenario?language=${currentLang}&difficulty=${duelDifficulty}`);
        if (!res.ok) throw new Error('Failed');
        duelProblem = await res.json();
        startDuel(duelProblem);
    } catch (err) { alert('Could not get challenge: ' + err.message); }
    btn.innerText = '⚔️ Start Duel';
    btn.disabled = false;
});

function startDuel(problem) {
    document.getElementById('duel-lobby').classList.add('hidden');
    document.getElementById('duel-arena').classList.remove('hidden');
    document.getElementById('duel-results').classList.add('hidden');

    const timeLimits = { easy: 300, medium: 180, hard: 120 };
    duelTimeLeft = problem.time_limit || timeLimits[duelDifficulty] || 180;

    document.getElementById('duel-problem-title').innerText = `${currentLang} Challenge — ${duelDifficulty.toUpperCase()}`;
    document.getElementById('duel-description').innerText = problem.description;
    document.getElementById('duel-code-editor').value = problem.default_code || LANGUAGE_CONFIG[currentLang].defaultCode;
    document.getElementById('duel-test-cases').value = problem.test_cases || '';

    updateDuelTimer();
    clearInterval(duelTimerInterval);
    duelTimerInterval = setInterval(() => {
        duelTimeLeft--;
        updateDuelTimer();
        if (duelTimeLeft <= 0) { clearInterval(duelTimerInterval); submitDuel(true); }
    }, 1000);
}

function updateDuelTimer() {
    const m = Math.floor(duelTimeLeft / 60);
    const s = duelTimeLeft % 60;
    const el = document.getElementById('duel-timer');
    el.innerText = `${m}:${s.toString().padStart(2, '0')}`;
    el.style.color = duelTimeLeft <= 30 ? 'var(--error)' : 'var(--warning)';
}

document.getElementById('duel-submit-btn').addEventListener('click', () => submitDuel(false));

async function submitDuel(timedOut = false) {
    clearInterval(duelTimerInterval);
    const code = document.getElementById('duel-code-editor').value;
    const test_cases = parseTestCases(document.getElementById('duel-test-cases').value);
    const timeUsed = (duelProblem?.time_limit || 180) - duelTimeLeft;

    const resultsDiv = document.getElementById('duel-results');
    resultsDiv.innerHTML = '<div style="color:var(--accent-primary)">Grading solution...</div>';
    resultsDiv.classList.remove('hidden');

    if (timedOut) {
        resultsDiv.innerHTML = `<div style="color:var(--error);font-weight:600;text-align:center;padding:1rem">⏰ Time's up! Better luck next time.</div>
            <button onclick="resetDuel()" class="btn-primary mt-4 full-width">Try Again</button>`;
        return;
    }

    try {
        const res = await fetch('/api/grade', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ code, test_cases, language: currentLang.toLowerCase() })
        });
        const r = await res.json();
        const passed = r.passed === r.total && r.total > 0;
        const minutes = Math.floor(timeUsed / 60);
        const seconds = timeUsed % 60;

        if (passed) { try { await fetch('/api/xp/award?event=duel_win', { method: 'POST' }); } catch(e) {} }
        else { try { await fetch('/api/xp/award?event=duel_complete', { method: 'POST' }); } catch(e) {} }

        resultsDiv.innerHTML = `
            <div style="text-align:center;padding:1rem;font-size:1.5rem">${passed ? '🏆' : '😤'}</div>
            <div class="metrics-grid">
                <div class="metric-card"><div class="metric-label">Result</div><div class="metric-value" style="color:${passed?'var(--success)':'var(--error)'};">${passed?'WIN':'LOSS'}</div></div>
                <div class="metric-card"><div class="metric-label">Tests Passed</div><div class="metric-value">${r.passed}/${r.total}</div></div>
                <div class="metric-card"><div class="metric-label">Time Used</div><div class="metric-value">${minutes}:${String(seconds).padStart(2,'0')}</div></div>
            </div>
            ${passed ? `<div style="color:var(--success);text-align:center;margin-top:1rem;font-weight:600">🎉 +30 XP earned!</div>` : ''}
            <button onclick="resetDuel()" class="btn-primary mt-4 full-width">Try Another Duel</button>`;
        loadXP();
    } catch (err) {
        resultsDiv.innerHTML = `<span style="color:var(--error)">Error: ${err.message}</span>`;
    }
}

window.resetDuel = function() {
    document.getElementById('duel-arena').classList.add('hidden');
    document.getElementById('duel-lobby').classList.remove('hidden');
    clearInterval(duelTimerInterval);
};

// ═══════════════════════════════ FEATURE 9: GITHUB REVIEW ════

document.getElementById('github-review-btn').addEventListener('click', async () => {
    const url = document.getElementById('github-url-input').value.trim();
    if (!url) { alert('Please enter a GitHub file URL'); return; }
    const statusEl = document.getElementById('github-status');
    const resultsEl = document.getElementById('github-results');
    const btn = document.getElementById('github-review-btn');
    btn.innerText = 'Fetching & Reviewing...';
    btn.disabled = true;
    statusEl.innerHTML = '<span style="color:var(--accent-primary)">🔍 Fetching code from GitHub...</span>';
    resultsEl.classList.add('hidden');

    try {
        const res = await fetch('/api/review-github', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url, language: currentLang.toLowerCase() })
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || 'Review failed');
        renderGithubReview(data);
        statusEl.innerText = '';
    } catch (err) {
        statusEl.innerHTML = `<span style="color:var(--error)">❌ ${err.message}</span>`;
    }
    btn.innerText = '🔍 Review Code';
    btn.disabled = false;
});

function renderGithubReview(d) {
    const resultsEl = document.getElementById('github-results');
    const ratingColor = parseInt(d.overall_rating) >= 7 ? 'var(--success)' : parseInt(d.overall_rating) >= 5 ? 'var(--warning)' : 'var(--error)';

    resultsEl.innerHTML = `
        <div class="glass-panel" style="padding:1.25rem;margin-bottom:1rem;display:flex;justify-content:space-between;align-items:center;">
            <div><div style="font-size:0.7rem;color:var(--text-secondary);margin-bottom:0.2rem">FILE</div><div style="font-weight:600">${d.filename}</div></div>
            <div style="text-align:center;"><div style="font-size:0.7rem;color:var(--text-secondary)">OVERALL RATING</div><div style="font-size:2rem;font-weight:700;color:${ratingColor}">${d.overall_rating}</div></div>
        </div>
        <div class="glass-panel" style="padding:1.25rem;margin-bottom:1rem;"><div style="font-size:0.9rem;line-height:1.6;color:var(--text-secondary)">${d.summary}</div></div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;">
            ${d.bugs?.length ? `<div class="glass-panel" style="padding:1.25rem;border-left:3px solid var(--error);">
                <div style="font-weight:600;color:var(--error);margin-bottom:0.6rem">🐛 Bugs Found</div>
                ${d.bugs.map(b => `<div style="font-size:0.88rem;margin-bottom:0.4rem;color:var(--text-secondary)">• ${b}</div>`).join('')}
            </div>` : `<div class="glass-panel" style="padding:1.25rem;border-left:3px solid var(--success);"><div style="color:var(--success)">✅ No bugs detected!</div></div>`}
            ${d.positive_highlights?.length ? `<div class="glass-panel" style="padding:1.25rem;border-left:3px solid var(--success);">
                <div style="font-weight:600;color:var(--success);margin-bottom:0.6rem">✦ Well Done</div>
                ${d.positive_highlights.map(h => `<div style="font-size:0.88rem;margin-bottom:0.4rem;color:var(--text-secondary)">• ${h}</div>`).join('')}
            </div>` : ''}
        </div>
        ${d.style_tips?.length ? `<div class="glass-panel" style="padding:1.25rem;margin-top:1rem;border-left:3px solid var(--accent-primary);">
            <div style="font-weight:600;color:var(--accent-primary);margin-bottom:0.6rem">🎨 Style Tips</div>
            ${d.style_tips.map(t => `<div style="font-size:0.88rem;margin-bottom:0.4rem;color:var(--text-secondary)">• ${t}</div>`).join('')}
        </div>` : ''}
        ${d.optimizations?.length ? `<div class="glass-panel" style="padding:1.25rem;margin-top:1rem;border-left:3px solid var(--warning);">
            <div style="font-weight:600;color:var(--warning);margin-bottom:0.6rem">⚡ Optimizations</div>
            ${d.optimizations.map(o => `<div style="font-size:0.88rem;margin-bottom:0.4rem;color:var(--text-secondary)">• ${o}</div>`).join('')}
        </div>` : ''}
        ${d.code_preview ? `<div class="glass-panel" style="padding:1.25rem;margin-top:1rem;">
            <div style="font-size:0.7rem;color:var(--text-secondary);margin-bottom:0.5rem">CODE PREVIEW</div>
            <pre style="background:var(--bg-base);padding:0.75rem;border-radius:6px;font-size:0.8rem;overflow-x:auto;max-height:300px"><code>${escapeHtml(d.code_preview)}</code></pre>
        </div>` : ''}`;
    resultsEl.classList.remove('hidden');
}

// ═══════════════════════════════ FEATURE 14: LEARNING PATH ═══

document.getElementById('generate-path-btn').addEventListener('click', async () => {
    const btn = document.getElementById('generate-path-btn');
    const resultsEl = document.getElementById('path-results');
    btn.innerText = 'Generating your path...';
    btn.disabled = true;
    resultsEl.innerHTML = '<div style="color:var(--accent-primary);text-align:center;padding:2rem">🗺️ Analyzing your mastery data and building your plan...</div>';
    resultsEl.classList.remove('hidden');

    try {
        const res = await fetch(`/api/learning-path?language=${currentLang}`);
        if (!res.ok) throw new Error('Failed');
        const data = await res.json();
        renderLearningPath(data.plan);
    } catch (err) {
        resultsEl.innerHTML = `<div style="color:var(--error)">Failed: ${err.message}</div>`;
    }
    btn.innerText = '✨ Generate My Learning Path';
    btn.disabled = false;
});

function renderLearningPath(plan) {
    const resultsEl = document.getElementById('path-results');
    resultsEl.innerHTML = plan.map((day, i) => {
        const storageKey = `path-day-${i}-${currentLang}`;
        const checked = localStorage.getItem(storageKey) === 'true' ? 'checked' : '';
        return `<div class="glass-panel path-day-card ${checked ? 'path-day-done' : ''}" style="padding:1.25rem;margin-bottom:0.75rem;border-left:3px solid ${checked ? 'var(--success)' : 'var(--accent-primary)'};">
            <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:0.6rem;">
                <div>
                    <div style="font-size:0.7rem;color:var(--text-secondary);margin-bottom:0.2rem">DAY ${day.day} OF 7</div>
                    <div style="font-weight:600;font-size:1rem;color:var(--accent-primary)">${day.topic}</div>
                </div>
                <label style="cursor:pointer;display:flex;align-items:center;gap:0.4rem;font-size:0.8rem;color:var(--text-secondary);">
                    <input type="checkbox" ${checked} onchange="togglePathDay(${i}, this.checked)" style="cursor:pointer"> Done
                </label>
            </div>
            <div style="font-size:0.85rem;color:var(--text-secondary);margin-bottom:0.5rem;line-height:1.5"><em>${day.why}</em></div>
            <div style="font-size:0.85rem;margin-bottom:0.4rem"><span style="color:var(--success);font-weight:500">🎯 Goal:</span> ${day.goal}</div>
            <div style="font-size:0.85rem;margin-bottom:0.4rem"><span style="color:var(--warning);font-weight:500">📝 Task:</span> ${day.mini_task}</div>
            <div style="font-size:0.82rem;color:var(--text-secondary);font-style:italic;margin-top:0.5rem">💡 ${day.tip}</div>
        </div>`;
    }).join('');
}

window.togglePathDay = function(dayIndex, checked) {
    localStorage.setItem(`path-day-${dayIndex}-${currentLang}`, checked);
    const cards = document.querySelectorAll('.path-day-card');
    if (cards[dayIndex]) {
        cards[dayIndex].style.borderLeftColor = checked ? 'var(--success)' : 'var(--accent-primary)';
        if (checked) cards[dayIndex].classList.add('path-day-done');
        else cards[dayIndex].classList.remove('path-day-done');
    }
};

// ═══════════════════════════════ FEATURE 5: XP & STREAK ══════

async function loadXP() {
    try {
        const res = await fetch('/api/xp');
        if (!res.ok) return;
        const data = await res.json();
        document.getElementById('xp-level-name').innerText = data.level_name;
        document.getElementById('xp-streak').innerText = `🔥 ${data.streak}`;
        document.getElementById('xp-total').innerText = `${data.total_xp} XP`;
        document.getElementById('xp-bar-fill').style.width = `${data.progress_pct}%`;
        if (data.xp_to_next) {
            document.getElementById('xp-next').innerText = `next: ${data.xp_to_next} XP`;
        } else {
            document.getElementById('xp-next').innerText = 'MAX LEVEL';
        }
    } catch (e) { /* silent */ }
}

// ── Utilities ────────────────────────────────────────────────
function escapeHtml(str) {
    return (str || '').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}

// ── Init ─────────────────────────────────────────────────────
updateHeader();
updateChatUI();
loadXP();
