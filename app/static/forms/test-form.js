const saveSurveyUrl = "http://localhost:42420/screenings/breast-cancer/v1/submit"
const surveyJson = {
  "pages": [
    {
      "name": "page00",
      "elements": [
        {
          "type": "panel",
          "name": "panel1",
          "elements": [
            {
              "type": "html",
              "name": "termOfUse",
              "html": "<video class='w-100' src='/media/canc/video.mp4' loop autoplay controls/>"
            },
            {
              "type": "boolean",
              "name": "video",
              "title": "ویدئوی آموزشی را مشاهده کردم",
              "titleLocation": "hidden",
              "hideNumber": true,
              "isRequired": true,
              "requiredErrorText": "برای ادامه می‌بایست ویدئوی بالا را مشاهده کنید.",
              "validators": [
                {
                  "type": "expression",
                  "text": "برای ادامه می‌بایست ویدئوی بالا را مشاهده کنید.",
                  "expression": "{video} = true"
                }
              ],
              "renderAs": "checkbox",
              "labelTrue": "بله",
              "labelFalse": "خیر"
            }
          ]
        }
      ]
    }
  ],
  "showQuestionNumbers": "off"
}
