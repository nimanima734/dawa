document.addEventListener('DOMContentLoaded', function() {
  const form = document.getElementById('productForm');

  form.addEventListener('submit', function(e) {
      e.preventDefault(); // نمنع الإرسال العادي

      // التحقق من الحقول المطلوبة
      const inputs = form.querySelectorAll('input, select, textarea');
      let isValid = true;

      inputs.forEach(input => {
          if (!input.value && input.hasAttribute('required')) {
              isValid = false;
              input.style.borderColor = 'red';
          } else {
              input.style.borderColor = '#ddd';
          }
      });

      if (isValid) {
          alert('Product saved successfully!');
          form.reset();
      } else {
          alert('Please fill all required fields!');
      }
  });
});
