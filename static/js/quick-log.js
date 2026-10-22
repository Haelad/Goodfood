// Быстрый дневник на карточках: «+» записывает обычную порцию, «−» отменяет
// последнюю сегодняшнюю. Итоги дня в нижней полосе обновляются из ответа.

// Повторный клик по той же кнопке быстрее этого порога — не отдельное
// нажатие, а «дребезг» кнопки мыши, тачпад или двойной клик (приходят
// через 30–60 мс). Осознанные быстрые нажатия идут от ~150 мс.
const REPEAT_GUARD_MS = 120;

function csrfToken() {
  const match = document.cookie.match(/(?:^|;\s*)csrftoken=([^;]+)/);
  return match ? decodeURIComponent(match[1]) : "";
}

function updateTotals(totals) {
  for (const [name, value] of Object.entries(totals)) {
    document.querySelectorAll(`[data-total="${name}"]`).forEach((el) => {
      el.textContent = value;
    });
  }
}

function render(control, count) {
  control.classList.toggle("has-count", count > 0);
  const counter = control.querySelector(".quick-log__count");
  counter.textContent = count;
  // короткий «щелчок» счётчика — подтверждение, что нажатие засчитано
  counter.classList.remove("bump");
  void counter.offsetWidth;
  counter.classList.add("bump");
}

document.addEventListener("click", (event) => {
  const button = event.target.closest(".quick-log__btn");
  if (!button) return;
  event.preventDefault(); // карточка целиком — ссылка, не открываем её

  const now = performance.now();
  if (now - (button._lastClick || -Infinity) < REPEAT_GUARD_MS) return;
  button._lastClick = now;

  const control = button.closest(".quick-log");
  const url = control.dataset[button.dataset.action === "eat" ? "eatUrl" : "uneatUrl"];

  // нажатия по одной карточке уходят строго по очереди
  control._queue = (control._queue || Promise.resolve())
    .then(() =>
      fetch(url, {
        method: "POST",
        headers: { "X-CSRFToken": csrfToken() },
        credentials: "same-origin",
      })
    )
    .then((response) => {
      if (!response.ok) throw new Error(response.status);
      return response.json();
    })
    .then((data) => {
      render(control, data.count);
      updateTotals(data.totals);
    })
    .catch(() => {
      control.classList.add("has-error");
      setTimeout(() => control.classList.remove("has-error"), 1200);
    });
});
