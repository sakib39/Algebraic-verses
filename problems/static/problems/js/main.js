document.addEventListener('DOMContentLoaded', function() {
    const cards = document.querySelectorAll('.card');
  
    cards.forEach(card => {
      card.addEventListener('click', function() {
        const categoryId = this.dataset.categoryId;
        window.location.href = `/categories/${categoryId}/`;
      });
    });
  });
  