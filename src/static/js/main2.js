console.log("test-test")

// new
// Get Stripe publishable key

fetch("http://localhost:8000/config/")
.then((result) => {return result.json(); })
.then((data) => {
    console.log(data.publicKey)
  // Initialize Stripe.js
  const stripe = Stripe(data.publicKey);
  console.log(stripe)

    // new
//   // Event handler
  document.querySelector("#submitBtn").addEventListener("click", (e) => {
    e.preventDefault();
//     // Get Checkout Session ID
    fetch("/create-checkout-session/")
    .then(response => response.json())
    .then((data) => {
        // data = data.json()
        console.log(data.sessionId)
        // Redirect to Stripe Checkout
        return stripe.redirectToCheckout({sessionId: data.sessionId})
    })
    // .then(() => {
    //   return e
    // });
  });
});

