document.querySelectorAll('.favourite-button').forEach(button => {
    button.addEventListener('click', () => {
        const productId = button.dataset.productId;
        fetch(`/favourite/${productId}`, { method: 'POST' })
    });
});