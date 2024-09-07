const survey = new Survey.Model(surveyJson);

function alertResults(sender) {
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

async function saveSurveyResults(saveUrl, displayUrl, json) {

    // Send POST request to FastAPI
    var response = await fetch(saveUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json;charset=UTF-8'
        },
        body: json
    })
    const responseJson = await response.json()

    console.log(responseJson)

    // Store the result in session storage (or any other storage)
    sessionStorage.setItem('result', JSON.stringify(responseJson));

    // Redirect to the results page
    window.location.href = displayUrl;
}
