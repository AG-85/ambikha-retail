document.addEventListener('DOMContentLoaded', function() {
    const searchForm = document.getElementById('search-form');
    const productResults = document.getElementById('product-results');
    const cartItems = document.getElementById('cart-items');
    const totalAmount = document.getElementById('total-amount');
    const checkoutButton = document.getElementById('checkout-button');
    const messageContainer = document.getElementById('message-container');
    const emptyCartMessage = document.getElementById('empty-cart-message');
    
    let cart = [];
    
    // Search form submission
    searchForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const formData = new FormData(searchForm);
        
        fetch('/search', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (!data.success) {
                showMessage(data.message, 'error');
                productResults.innerHTML = '';
                return;
            }
            
            displayProducts(data.products);
        })
        .catch(error => {
            console.error('Error:', error);
            showMessage('An unexpected error occurred. Please try again.', 'error');
        });
    });
    
    // Display products
    function displayProducts(products) {
        productResults.innerHTML = '';
        
        if (products.length === 0) {
            productResults.innerHTML = '<p>No products found</p>';
            return;
        }
        
        products.forEach(product => {
            const productElement = document.createElement('div');
            productElement.className = 'product-item';
            productElement.innerHTML = `
                <div class="product-details">
                    <div class="product-name">${product.name}</div>
                    <div class="product-price">$${product.price.toFixed(2)}</div>
                    <div class="product-stock">${product.stock > 0 ? 'In Stock' : 'Out of Stock'}</div>
                </div>
                <div class="product-actions">
                    <input type="number" class="quantity-input" min="1" max="${product.stock}" value="1" ${product.stock === 0 ? 'disabled' : ''}>
                    <button class="add-to-cart" data-product-id="${product.id}" ${product.stock === 0 ? 'disabled' : ''}>Add to Cart</button>
                </div>
            `;
            
            productResults.appendChild(productElement);
            
            // Add event listener to the Add to Cart button
            const addToCartButton = productElement.querySelector('.add-to-cart');
            addToCartButton.addEventListener('click', function() {
                const quantityInput = productElement.querySelector('.quantity-input');
                const quantity = parseInt(quantityInput.value);
                
                const formData = new FormData();
                formData.append('product_id', product.id);
                formData.append('quantity', quantity);
                
                fetch('/add-to-cart', {
                    method: 'POST',
                    body: formData
                })
                .then(response => response.json())
                .then(data => {
                    if (!data.success) {
                        showMessage(data.message, 'error');
                        return;
                    }
                    
                    cart = data.cart;
                    updateCartDisplay();
                    showMessage(data.message, 'success');
                })
                .catch(error => {
                    console.error('Error:', error);
                    showMessage('An unexpected error occurred. Please try again.', 'error');
                });
            });
        });
    }
    
    // Update cart display
    function updateCartDisplay() {
        if (cart.length === 0) {
            emptyCartMessage.style.display = 'block';
            checkoutButton.disabled = true;
            cartItems.innerHTML = emptyCartMessage.outerHTML;
            totalAmount.textContent = '0.00';
            return;
        }
        
        emptyCartMessage.style.display = 'none';
        checkoutButton.disabled = false;
        
        let cartHTML = '';
        let total = 0;
        
        cart.forEach(item => {
            const itemTotal = item.price * item.quantity;
            total += itemTotal;
            
            cartHTML += `
                <div class="cart-item">
                    <span>${item.name} x ${item.quantity}</span>
                    <span>$${itemTotal.toFixed(2)}</span>
                </div>
            `;
        });
        
        cartItems.innerHTML = cartHTML;
        totalAmount.textContent = total.toFixed(2);
    }
    
    // Checkout button
    checkoutButton.addEventListener('click', function() {
        fetch('/checkout', {
            method: 'POST'
        })
        .then(response => response.json())
        .then(data => {
            if (!data.success) {
                showMessage(data.message, 'error');
                return;
            }
            
            cart = [];
            updateCartDisplay();
            showMessage(data.message, 'success');
        })
        .catch(error => {
            console.error('Error:', error);
            showMessage('An unexpected error occurred. Please try again.', 'error');
            // For testing the webpage crash scenario
            if (Math.random() < 0.1) {
                window.location.href = '/';
            }
        });
    });
    
    // Display message
    function showMessage(message, type) {
        messageContainer.textContent = message;
        messageContainer.className = 'message-container ' + type + '-message';
        
        // Auto hide after 5 seconds
        setTimeout(() => {
            messageContainer.textContent = '';
            messageContainer.className = 'message-container';
        }, 5000);
    }
    
    // Initialize
    updateCartDisplay();
});