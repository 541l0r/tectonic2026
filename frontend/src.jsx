import React, { useState } from 'react';
import { createRoot } from 'react-dom/client';
import './style.css';

function Block({ block }) {
  if (block.type === 'metric') return <section className="card"><small>{block.label}</small><strong>{block.value}</strong><span>{block.detail}</span></section>;
  if (block.type === 'list' && Array.isArray(block.items)) return <section className="card"><h2>{block.title}</h2><ul>{block.items.map((item, i) => <li key={i}>{item}</li>)}</ul></section>;
  if (block.type === 'text') return <p>{block.text}</p>;
  return null;
}

function App() {
  const [message, setMessage] = useState('What changed in my spending?');
  const [response, setResponse] = useState(null);
  const [error, setError] = useState('');
  const [busy, setBusy] = useState(false);

  async function submit(event) {
    event.preventDefault();
    setBusy(true); setError(''); setResponse(null);
    try {
      const result = await fetch('/api/ask', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ message, user_id: 'demo' }) });
      const body = await result.json();
      if (!result.ok) throw new Error(body.error || 'Request failed');
      setResponse(body);
    } catch (e) { setError(e.message); }
    finally { setBusy(false); }
  }

  return <main><header><span className="eyebrow">TECTONIC / WORKING SLICE</span><h1>Ask. Understand. Act.</h1><p>Mock data, real interface contract. Adapt the product when the challenge arrives.</p></header><form onSubmit={submit}><label htmlFor="request">Your question</label><div className="row"><input id="request" value={message} maxLength={2000} onChange={e => setMessage(e.target.value)} required /><button disabled={busy}>{busy ? 'Working…' : 'Ask'}</button></div></form>{error && <p role="alert" className="error">{error}</p>}{response && <article aria-live="polite"><p className="answer">{response.answer}</p><div className="blocks">{Array.isArray(response.blocks) && response.blocks.map((block, i) => <Block block={block} key={i} />)}</div><small>Source: {response.source}</small></article>}</main>;
}

createRoot(document.getElementById('root')).render(<App />);
