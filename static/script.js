document.addEventListener("DOMContentLoaded", function () {

    // ==========================================
    // QUESTIONS
    // ==========================================

    const questions = [

        [
            "city",
            "📍 Which city is the property located in?"
        ],

        [
            "propertyType",
            "🏠 What is the property type? Example: Apartment, Villa, Independent House"
        ],

        [
            "bedrooms",
            "🛏️ How many bedrooms does the property have?"
        ],

        [
            "bathrooms",
            "🚿 How many bathrooms does the property have?"
        ],

        [
            "carpetArea",
            "📐 What is the carpet area in sq.ft? Example: 1200"
        ],

        [
            "furnishing",
            "🛋️ What is the furnishing status? Example: Furnished, Semi-Furnished, Unfurnished"
        ],

        [
            "flrNum",
            "🏢 Which floor is the property on? Example: Ground, 1, 2, 3"
        ],

        [
            "totalFlrNum",
            "🏙️ What is the total number of floors in the building?"
        ],

        [
            "facing",
            "🧭 What is the property facing? Example: East, West, North, South"
        ]

    ];


    let currentQuestion = 0;

    let houseData = {};


    // ==========================================
    // HTML ELEMENTS
    // ==========================================

    const chatBox =
        document.getElementById("chatBox");

    const userInput =
        document.getElementById("userInput");

    const sendBtn =
        document.getElementById("sendBtn");

    const progressBar =
        document.getElementById("progressFill");

    const progressText =
        document.getElementById("progressText");


    // ==========================================
    // BOT MESSAGE
    // ==========================================

    function addBotMessage(message) {

        const messageDiv =
            document.createElement("div");

        messageDiv.className =
            "message bot-message";

        messageDiv.innerHTML = `
            <div class="avatar">🤖</div>

            <div class="bubble">
                ${message}
            </div>
        `;

        chatBox.appendChild(messageDiv);

        chatBox.scrollTop =
            chatBox.scrollHeight;
    }


    // ==========================================
    // USER MESSAGE
    // ==========================================

    function addUserMessage(message) {

        const messageDiv =
            document.createElement("div");

        messageDiv.className =
            "message user-message";

        messageDiv.innerHTML = `
            <div class="bubble">
                ${message}
            </div>
        `;

        chatBox.appendChild(messageDiv);

        chatBox.scrollTop =
            chatBox.scrollHeight;
    }


    // ==========================================
    // PROGRESS
    // ==========================================

    function updateProgress() {

        const total =
            questions.length;

        progressText.innerText =
            `${currentQuestion} / ${total}`;

        const percentage =
            (currentQuestion / total) * 100;

        progressBar.style.width =
            `${percentage}%`;
    }


    // ==========================================
    // SHOW QUESTION
    // ==========================================

    function showQuestion() {

        if (currentQuestion >= questions.length) {

            predictPrice();

            return;
        }


        const question =
            questions[currentQuestion][1];

        addBotMessage(question);

        userInput.focus();
    }


    // ==========================================
    // VALIDATE INPUT
    // ==========================================

    function validateInput(key, value) {

        value = value.trim();


        // CITY
        if (key === "city") {

            if (value === "") {

                return "Please enter a city name.";
            }
        }


        // PROPERTY TYPE
        if (key === "propertyType") {

            if (value === "") {

                return "Please enter the property type.";
            }
        }


        // BEDROOMS
        if (key === "bedrooms") {

            const number =
                Number(value);

            if (
                isNaN(number) ||
                number <= 0 ||
                number > 20
            ) {

                return "Please enter a valid number of bedrooms. Example: 3";
            }
        }


        // BATHROOMS
        if (key === "bathrooms") {

            const number =
                Number(value);

            if (
                isNaN(number) ||
                number <= 0 ||
                number > 20
            ) {

                return "Please enter a valid number of bathrooms. Example: 2";
            }
        }


        // CARPET AREA
        if (key === "carpetArea") {

            const number =
                Number(value);

            if (
                isNaN(number) ||
                number <= 0
            ) {

                return "Please enter a valid carpet area. Example: 1200";
            }
        }


        // FURNISHING
        if (key === "furnishing") {

            if (value === "") {

                return "Please enter furnishing status. Example: Furnished";
            }
        }


        // FLOOR NUMBER
        if (key === "flrNum") {

            const lower =
                value.toLowerCase();

            if (lower !== "ground") {

                const number =
                    Number(value);

                if (
                    isNaN(number) ||
                    number < 0
                ) {

                    return "Please enter a valid floor number. Example: Ground or 3";
                }
            }
        }


        // TOTAL FLOORS
        if (key === "totalFlrNum") {

            const number =
                Number(value);

            if (
                isNaN(number) ||
                number <= 0
            ) {

                return "Please enter a valid total number of floors. Example: 6";
            }
        }


        // FACING
        if (key === "facing") {

            if (value === "") {

                return "Please enter the facing direction. Example: East";
            }
        }


        return null;
    }


    // ==========================================
    // SEND MESSAGE
    // ==========================================

    function sendMessage() {

        const message =
            userInput.value.trim();


        // Empty input
        if (message === "") {

            return;
        }


        // All questions completed
        if (
            currentQuestion >=
            questions.length
        ) {

            return;
        }


        // Current question key
        const key =
            questions[currentQuestion][0];


        // Validate
        const error =
            validateInput(key, message);


        if (error) {

            addBotMessage(
                "❌ " + error
            );

            userInput.value = "";

            userInput.focus();

            return;
        }


        // Display user answer
        addUserMessage(message);


        // Save answer
        houseData[key] = message;


        // Clear input
        userInput.value = "";


        // Next question
        currentQuestion++;


        // Update progress
        updateProgress();


        // Show next question
        setTimeout(function () {

            showQuestion();

        }, 400);
    }


    // ==========================================
    // PREDICT PRICE
    // ==========================================

    async function predictPrice() {

        addBotMessage(
            "⏳ Please wait... I am calculating the estimated house price."
        );


        try {

            const response =
                await fetch("/predict", {

                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({

                        propertyType:
                            houseData.propertyType,

                        furnishing:
                            houseData.furnishing,

                        flrNum:
                            houseData.flrNum,

                        facing:
                            houseData.facing,

                        totalFlrNum:
                            Number(
                                houseData.totalFlrNum
                            ),

                        city:
                            houseData.city,

                        carpetArea:
                            Number(
                                houseData.carpetArea
                            ),

                        bedrooms:
                            Number(
                                houseData.bedrooms
                            ),

                        bathrooms:
                            Number(
                                houseData.bathrooms
                            )

                    })
                });


            const result =
                await response.json();


            // ==================================
            // ERROR RESPONSE
            // ==================================

            if (!response.ok) {

                addBotMessage(
                    "❌ " +
                    (
                        result.error ||
                        "Error while predicting house price."
                    )
                );

                return;
            }


            // ==================================
            // PRICE
            // ==================================

            const price =
                Number(result.price);


            // Indian number format
            const formattedPrice =
                price.toLocaleString(
                    "en-IN",
                    {
                        minimumFractionDigits: 2,
                        maximumFractionDigits: 2
                    }
                );


            // ==================================
            // RESULT
            // ==================================

            addBotMessage(`

                <div class="price-card">

                    <h3>
                        🏠 Estimated House Price
                    </h3>

                    <div class="price">
                        ₹${formattedPrice}
                    </div>

                    <p>
                        This is the estimated price
                        based on your property details.
                    </p>

                </div>

            `);


            // ==================================
            // COMPLETED
            // ==================================

            progressText.innerText =
                "Completed ✓";

            progressBar.style.width =
                "100%";


        } catch (error) {

            console.error(
                "Prediction Error:",
                error
            );

            addBotMessage(
                "❌ Unable to connect with the Flask server."
            );
        }
    }


    // ==========================================
    // SEND BUTTON
    // ==========================================

    sendBtn.addEventListener(
        "click",
        sendMessage
    );


    // ==========================================
    // ENTER KEY
    // ==========================================

    userInput.addEventListener(
        "keydown",
        function (event) {

            if (event.key === "Enter") {

                event.preventDefault();

                sendMessage();
            }
        }
    );


    // ==========================================
    // RESTART CHAT
    // ==========================================

    window.restartChat = function () {

        currentQuestion = 0;

        houseData = {};

        chatBox.innerHTML = "";

        progressText.innerText =
            "0 / 9";

        progressBar.style.width =
            "0%";


        addBotMessage(
            "👋 Welcome back! I am your House Price Prediction Assistant."
        );


        setTimeout(function () {

            showQuestion();

        }, 500);
    };


    // ==========================================
    // START CHATBOT
    // ==========================================

    updateProgress();


    addBotMessage(
        "👋 Hello! I am your House Price Prediction Assistant."
    );


    setTimeout(function () {

        showQuestion();

    }, 500);

});