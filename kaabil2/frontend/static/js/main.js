document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("input, select, textarea").forEach((el) => {
    if (!el.classList.contains("form-control") && el.type !== "radio" && el.type !== "checkbox" && el.type !== "hidden" && el.type !== "submit") el.classList.add("form-control");
  });
});
