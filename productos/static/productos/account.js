document.addEventListener('DOMContentLoaded', function() {
  const switchInput = document.getElementById('crearCuenta');
  const passwordGroup = document.getElementById('campoPassword');
  if (switchInput) {
    switchInput.addEventListener('change', function() {
      if (passwordGroup) {
        passwordGroup.classList.toggle('d-none', !this.checked);
      }
    });
  }
});
