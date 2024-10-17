(() =>
  [...document.querySelectorAll(".form-controls")].forEach((el) =>
    [...el.children].forEach((child) =>
      child.setAttribute(":disabled", "submitting")
    )
  ))();
