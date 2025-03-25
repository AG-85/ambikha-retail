Feature: Product management and shopping cart functionality
  As a customer of the online store
  I want to be able to search for products, add them to cart, and checkout
  So that I can purchase items online

  Scenario: Successfully search and purchase a single product
    Given I am on the product display page
    When I search for a valid product
    And I add the product to the cart
    And I checkout
    Then I should be redirected to the homepage

  Scenario: Successfully search and purchase multiple quantity product
    Given I am on the product display page
    When I search for a valid product
    And I add multiple quantities of the product to the cart
    And I checkout
    Then I should be redirected to the homepage

  Scenario: Adding multiple products to the cart and checking out
    Given I am on the product display page
    When I search for multiple valid products
    And I add the products to the cart
    And I checkout
    Then I should be redirected to the homepage

  Scenario: Attempt to checkout with an empty cart
    Given I am on the product display page
    When I try to checkout with an empty cart
    Then I should see an error message that the cart is empty

  Scenario: Attempting to add a product to the cart with quantity 0
    Given I am on the product display page
    When I search for a valid product
    And I set the quantity to 0
    And I click the Add to Cart button
    Then I should see an error message about invalid quantity

  Scenario: Enter the correct product name and the product is not found
    Given I am on the product display page
    When I search for a product that does not exist
    Then I should see an error message that the product was not found

  Scenario: Product is out of stock during checkout
    Given I am on the product display page
    When I search for a valid product
    And I add the product to the cart
    And the product goes out of stock before I complete my purchase
    Then I should see an error message that the product is out of stock

  Scenario: Webpage crashes upon clicking the checkout button
    Given I am on the product display page
    When I search for a valid product
    And I add the product to the cart
    And an error occurs during checkout
    Then I should see a webpage crash error˘