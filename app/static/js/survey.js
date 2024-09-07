const survey = new Survey.Model(surveyJson);

function alertResults(sender, options) {
    const results = JSON.stringify({survey_response: sender.data});
    alert(results);
    saveSurveyResults(saveSurveyUrl,
        displayResultsUrl,
        results
    )
}

survey.onComplete.add(alertResults);

document.addEventListener("DOMContentLoaded", function () {
    survey.render(document.getElementById("surveyContainer"));
});

function saveSurveyResults(saveUrl, displayUrl, json) {

    // Send POST request to FastAPI
    var response = fetch(saveUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json;charset=UTF-8'
        },
        body: json
    })

    console.log(JSON.stringify(response.data))

    // Store the result in session storage (or any other storage)
    sessionStorage.setItem('result', JSON.stringify(response.data));

    // Redirect to the results page
    // window.location.href = displayUrl;
}

// function saveSurveyResults(saveUrl, displayUrl, json) {
//
//     fetch(saveUrl, {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json;charset=UTF-8'
//         },
//         body: json
//     })
//     .then(response => {
//         if (response.ok) {
//             fetch(displayUrl, {method: 'GET', headers: {'Content-Type': 'application/json;charset=UTF-8'}})
//         } else {
//             // Handle error
//         }
//     })
//     .catch(error => {
//     });
// }