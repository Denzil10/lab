// Lab signals: posts a like, subscribe or unsubscribe email, feedback or idea to a Google Form (docs: lab README).
(() => {
  const FORM = "https://docs.google.com/forms/d/e/1FAIpQLSdvfY4HsiHT-1tpRGDg9jFBU5rEY5zu9IFSai8OsoSpmkxaew/formResponse", ENTRY = {"app": "entry.455481753", "kind": "entry.919979920", "email": "entry.121800902", "text": "entry.542581525"};
  const send = (app, kind, fields = {}) => {
    const body = new URLSearchParams({[ENTRY.app]: app, [ENTRY.kind]: kind});
    for (const [k, v] of Object.entries(fields)) body.set(ENTRY[k], v);
    return fetch(FORM, {method: "POST", mode: "no-cors", body});
  };
  for (const b of document.querySelectorAll("button[data-like]")) {
    const key = "lab-liked:" + b.dataset.like;
    const done = () => { b.disabled = true; b.textContent = "♥ Liked"; };
    if (localStorage.getItem(key)) done();
    b.addEventListener("click", () => {
      done();  // before the request, so a double tap sends one like
      send(b.dataset.like, "like").then(() => {
        localStorage.setItem(key, "1");
        if (!localStorage.getItem("lab-subscribed"))
          b.insertAdjacentHTML("afterend", ' <a class="after" href="#subscribe">get the next one first ↓</a>');
      }, () => { b.disabled = false; b.textContent = "♥ I like it"; });
    });
  }
  for (const f of document.querySelectorAll("form[data-kind]")) {
    f.addEventListener("submit", e => {
      e.preventDefault();
      const fields = {};
      for (const el of f.elements) if (el.name && el.value.trim()) fields[el.name] = el.value.trim();
      if (!Object.keys(fields).length) return;
      const note = f.querySelector(".sent");
      send(f.dataset.app, f.dataset.kind, fields).then(() => {
        f.reset();
        note.textContent = f.dataset.done || "Sent. Thank you.";
        if (f.dataset.kind === "subscribe") localStorage.setItem("lab-subscribed", "1");
      }, () => { note.textContent = "Could not send; try again."; });
    });
  }
  // The unsubscribe link in each email carries the address: send it on load.
  const unsub = document.querySelector('form[data-kind="unsubscribe"]');
  const email = new URLSearchParams(location.search).get("email");
  if (unsub && email) { unsub.elements.email.value = email; unsub.requestSubmit(); }
})();
