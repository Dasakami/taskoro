document.addEventListener('DOMContentLoaded', function() {
    // Chest hover effects
    const chestCards = document.querySelectorAll('.chest-card');
    
    chestCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
            this.style.boxShadow = '0 12px 25px rgba(0, 0, 0, 0.3)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '0 8px 15px rgba(0, 0, 0, 0.2)';
        });
    });
    
    // Chest opening animation
    const openChestButtons = document.querySelectorAll('.open-chest-button');
    const chestModal = document.getElementById('chest-opening-modal');
    const closeButton = document.getElementById('close-chest-modal');
    
    if (openChestButtons.length > 0) {
        openChestButtons.forEach(button => {
            button.addEventListener('click', function(e) {
                e.preventDefault();
                
                // Set the appropriate chest icon
                const chestId = this.getAttribute('data-chest-id');
                const chestCard = this.closest('.chest-card');
                const chestRarity = chestCard.getAttribute('data-rarity');
                const chestIconLarge = chestModal.querySelector('.chest-icon-large');
                
                if (chestRarity === 'common') {
                    chestIconLarge.textContent = '📦';
                } else if (chestRarity === 'rare') {
                    chestIconLarge.textContent = '🎁';
                } else if (chestRarity === 'epic') {
                    chestIconLarge.textContent = '💎';
                } else if (chestRarity === 'legendary') {
                    chestIconLarge.textContent = '👑';
                }
                
                // Show the modal
                chestModal.style.display = 'flex';
                
                // Hide rewards and show opening animation
                const openingText = chestModal.querySelector('.opening-text');
                const rewardsContainer = chestModal.querySelector('.rewards-container');
                
                openingText.style.display = 'block';
                rewardsContainer.style.display = 'none';
                
                // Simulate chest opening (would be replaced with actual data from the server)
                setTimeout(function() {
                    openingText.style.display = 'none';
                    rewardsContainer.style.display = 'block';
                    
                    // Set random reward amounts (this would come from server)
                    const coinRewardAmount = chestModal.querySelector('#coin-reward-amount');
                    const gemRewardAmount = chestModal.querySelector('#gem-reward-amount');
                    
                    let coinReward, gemReward;
                    
                    if (chestRarity === 'common') {
                        coinReward = Math.floor(Math.random() * 50) + 50;
                        gemReward = Math.floor(Math.random() * 5) + 1;
                    } else if (chestRarity === 'rare') {
                        coinReward = Math.floor(Math.random() * 100) + 100;
                        gemReward = Math.floor(Math.random() * 10) + 5;
                    } else if (chestRarity === 'epic') {
                        coinReward = Math.floor(Math.random() * 200) + 200;
                        gemReward = Math.floor(Math.random() * 15) + 10;
                    } else if (chestRarity === 'legendary') {
                        coinReward = Math.floor(Math.random() * 500) + 500;
                        gemReward = Math.floor(Math.random() * 30) + 20;
                    }
                    
                    // Animation for counting up the rewards
                    let currentCoins = 0;
                    let currentGems = 0;
                    
                    const coinInterval = setInterval(function() {
                        currentCoins += Math.ceil(coinReward / 20);
                        if (currentCoins >= coinReward) {
                            currentCoins = coinReward;
                            clearInterval(coinInterval);
                        }
                        coinRewardAmount.textContent = currentCoins;
                    }, 50);
                    
                    const gemInterval = setInterval(function() {
                        currentGems += Math.ceil(gemReward / 20);
                        if (currentGems >= gemReward) {
                            currentGems = gemReward;
                            clearInterval(gemInterval);
                        }
                        gemRewardAmount.textContent = currentGems;
                    }, 50);
                    
                }, 2000);
                
                // Submit the form after animations
                setTimeout(function() {
                    const form = button.closest('form');
                    if (form) {
                        form.submit();
                    }
                }, 6000);
            });
        });
    }
    
    if (closeButton) {
        closeButton.addEventListener('click', function() {
            chestModal.style.display = 'none';
        });
    }
    
    // Close modal when clicking outside
    window.addEventListener('click', function(e) {
        if (e.target === chestModal) {
            chestModal.style.display = 'none';
        }
    });
});