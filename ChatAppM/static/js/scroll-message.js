document.addEventListener('DOMContentLoaded', () =>{
  const element = document.getElementById("message-area");
  if (!element) return;

  element.scrollTop = element.scrollHeight;
});
