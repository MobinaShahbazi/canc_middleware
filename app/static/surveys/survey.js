{
  "title": "NPS Survey Question",
  "completedHtml": "<h3>Thank you for your feedback</h3>",
  "completedHtmlOnCondition": [
    {
      "expression": "{nps_score} >= 9",
      "html": "<h3>Thank you for your feedback</h3> <h4>We are glad that you love our product. Your ideas and suggestions will help us make it even better.</h4>"
    },
    {
      "expression": "{nps_score} >= 6  and {nps_score} <= 8",
      "html": "<h3>Thank you for your feedback</h3> <h4>We are glad that you shared your ideas with us. They will help us make our product better.</h4>"
    }
  ],
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
    },
    {
      "name": "page1",
      "title": "اطلاعات کلی",
      "elements": [
        {
          "type": "panel",
          "name": "panel_cancq1",
          "elements": [
            {
              "type": "text",
              "name": "birth_year",
              "title": "متولد چه سالی هستید؟",
              "isRequired": true,
              "inputType": "number",
              "min": 1300,
              "max": 1394,
              "minErrorText": "حداقل مقدار سال 1300 است",
              "maxErrorText": "حداکثر مقدار سال 1394 است"
            },
            {
              "type": "text",
              "name": "birth_month",
              "title": "متولد چه ماهی هستید؟",
              "isRequired": true,
              "inputType": "number",
              "min": 1,
              "max": 12,
              "minErrorText": "حداقل مقدار ماه 1 است",
              "maxErrorText": "حداکثر مقدار ماه 12 است"
            }
          ]
        },
        {
          "type": "panel",
          "name": "panel_cancq8",
          "elements": [
            {
              "type": "dropdown",
              "name": "province_residence",
              "title": "استان محل سکونت",
              "isRequired": true,
              "choices": [
                "اردبیل",
                "اصفهان",
                "البرز",
                "ایلام",
                "آذربایجان شرقی",
                "آذربایجان غربی",
                "بوشهر",
                "تهران",
                "چهارمحال و بختیاری",
                "خراسان جنوبی",
                "خراسان رضوی",
                "خراسان شمالی",
                "خوزستان",
                "زنجان",
                "سمنان",
                "سیستان و بلوچستان",
                "فارس",
                "قزوین",
                "قم",
                "کردستان",
                "کرمان",
                "کرمانشاه",
                "کهگیلویه و بویراحمد",
                "گلستان",
                "گیلان",
                "لرستان",
                "مازندران",
                "مرکزی",
                "هرمزگان",
                "همدان",
                "یزد",
                "خارج از ایران"
              ]
            }
          ]
        },
        {
          "type": "panel",
          "name": "panel_cancq2",
          "elements": [
            {
              "type": "text",
              "name": "height",
              "title": "قد شما چقدر است؟ (سانتیمتر)",
              "isRequired": true,
              "inputType": "number",
              "min": 100,
              "max": 220,
              "minErrorText": "حداقل مقدار قد 100 (سانتیمتر) است",
              "maxErrorText": "حداکثر مقدار قد 220 (سانتیمتر) است"
            }
          ]
        },
        {
          "type": "panel",
          "name": "panel_cancq3",
          "elements": [
            {
              "type": "text",
              "name": "weight",
              "title": "وزن شما چقدر است؟ (کیلوگرم)",
              "isRequired": true,
              "inputType": "number",
              "min": 40,
              "max": 150,
              "minErrorText": "حداقل مقدار وزن 40 (کیلوگرم) است",
              "maxErrorText": "حداکثر مقدار وزن 150 (کیلوگرم) است"
            }
          ]
        },
        {
          "type": "panel",
          "name": "panel_cancq4",
          "elements": [
            {
              "type": "text",
              "name": "cancq4",
              "title": "شروع قاعدگی (اولین قاعدگی) شما در چه سنی بوده است؟ (سال)",
              "isRequired": true,
              "inputType": "number",
              "min": 7,
              "max": 60,
              "minErrorText": "حداقل مقدار قابل قبول 7 است",
              "maxErrorText": "حداکثر مقدار قابل قبول 60 است"
            }
          ]
        },
        {
          "type": "panel",
          "name": "panel3",
          "elements": [
            {
              "type": "radiogroup",
              "name": "child_birth_history",
              "title": "آیا سابقه به دنیا آوردن فرزند دارید؟",
              "isRequired": true,
              "choices": [
                {
                  "value": "false",
                  "text": "خیر"
                },
                {
                  "value": "true",
                  "text": "بله"
                }
              ]
            },
            {
              "type": "text",
              "name": "child_birth_first_age",
              "visibleIf": "{cancq5} = true",
              "title": "سن اولین بارداری خود را ذکر کنید (سال)",
              "isRequired": true,
              "inputType": "number",
              "min": 13,
              "max": 60,
              "minErrorText": "حداقل مقدار قابل قبول 13 است",
              "maxErrorText": "حداکثر مقدار قابل قبول 60 است"
            }
          ]
        },
        {
          "type": "panel",
          "name": "panel2",
          "elements": [
            {
              "type": "radiogroup",
              "name": "smoking_history",
              "title": "آیا هیچ گاه دخانیات (شامل سیگار، قلیان، پیپ، ویپ و ...) مصرف کرده اید؟",
              "isRequired": true,
              "choices": [
                {
                  "value": "false",
                  "text": "خیر"
                },
                {
                  "value": "before",
                  "text": "مصرف می کرده ام و در حال حاضر مصرف نمی کنم"
                },
                {
                  "value": "now",
                  "text": "در حال حاضر مصرف می کنم"
                }
              ]
            },
            {
              "type": "radiogroup",
              "name": "cancq6_2",
              "visibleIf": "{smoking_history} = 'before'",
              "title": "به چه میزان دخانیات مصرف می کردید؟",
              "isRequired": true,
              "choices": [
                {
                  "value": "1",
                  "text": "به طور مداوم و روزانه"
                },
                {
                  "value": "2",
                  "text": "چند بار در هفته"
                },
                {
                  "value": "3",
                  "text": "چند بار درماه"
                },
                {
                  "value": "4",
                  "text": "سالی چند بار و تفننی"
                }
              ]
            },
            {
              "type": "radiogroup",
              "name": "smoking_frequency",
              "visibleIf": "{smoking_history} = 'now'",
              "title": "به چه میزان دخانیات مصرف میکنید؟",
              "isRequired": true,
              "choices": [
                {
                  "value": "1",
                  "text": "به طور مداوم و روزانه"
                },
                {
                  "value": "2",
                  "text": "چند بار در هفته"
                },
                {
                  "value": "3",
                  "text": "چند بار درماه"
                },
                {
                  "value": "4",
                  "text": "سالی چند بار و تفننی"
                }
              ]
            }
          ]
        },
        {
          "type": "panel",
          "name": "panel4",
          "elements": [
            {
              "type": "radiogroup",
              "name": "contraceptive_history",
              "title": "آیا سابقه مصرف قرص ضدبارداری خوراکی یا هورمون درمانی جایگزین (پس از یائسگی) دارید؟",
              "isRequired": true,
              "choices": [
                {
                  "value": "1",
                  "text": "هرگز استفاده نکرده ام"
                },
                {
                  "value": "2",
                  "text": "مصرف می کرده ام و از قطع مصرف آن بیش از 5 سال گذشته است"
                },
                {
                  "value": "3",
                  "text": "در طی 5 سال گذشته مصرف می کرده ام و اکنون مصرف نمی کنم"
                },
                {
                  "value": "4",
                  "text": "هم اکنون مصرف می کنم"
                }
              ]
            },
            {
              "type": "text",
              "name": "contraceptive_history_years",
              "visibleIf": "{contraceptive_history} anyof [2, 3, 4]",
              "title": "تعداد سال های مصرف را ذکر کنید (سال)",
              "isRequired": true,
              "inputType": "number",
              "min": 1,
              "max": 40,
              "minErrorText": "حداقل مقدار قابل قبول 1 است",
              "maxErrorText": "حداکثر مقدار قابل قبول 40 است"
            }
          ]
        }
      ]
    },
    {
      "name": "page2",
      "title": "سوابق پزشکی فردی",
      "elements": [
        {
          "type": "panel",
          "name": "panel40",
          "elements": [
            {
              "type": "radiogroup",
              "name": "clinical_examination_history",
              "title": "آیا تاکنون معاینه پستان توسط پزشک برای شما انجام شده است؟",
              "isRequired": true,
              "choices": [
                {
                  "value": "false",
                  "text": "خیر"
                },
                {
                  "value": "true",
                  "text": "بله"
                }
              ]
            },
            {
              "type": "text",
              "name": "clinical_examination_count",
              "visibleIf": "{clinical_examination_history} = true",
              "title": "چند نوبت؟",
              "isRequired": true,
              "inputType": "number"
            },
            {
              "type": "text",
              "name": "clinical_examination_year",
              "visibleIf": "{clinical_examination_history} = true",
              "title": "سال",
              "isRequired": true,
              "inputType": "number",
              "min": 1300,
              "max": 1402,
              "minErrorText": "حداقل مقدار سال 1300 است",
              "maxErrorText": "حداکثر مقدار سال 1402 است"
            },
            {
              "type": "dropdown",
              "name": "clinical_examination_month",
              "visibleIf": "{clinical_examination_history} = true",
              "startWithNewLine": false,
              "title": "ماه",
              "isRequired": true,
              "choices": [
                {
                  "value": "01",
                  "text": "فروردین"
                },
                {
                  "value": "02",
                  "text": "اردیبهشت"
                },
                {
                  "value": "03",
                  "text": "خرداد"
                },
                {
                  "value": "04",
                  "text": "تیر"
                },
                {
                  "value": "05",
                  "text": "مرداد"
                },
                {
                  "value": "06",
                  "text": "شهریور"
                },
                {
                  "value": "07",
                  "text": "مهر"
                },
                {
                  "value": "08",
                  "text": "آبان"
                },
                {
                  "value": "09",
                  "text": "آذر"
                },
                {
                  "value": "10",
                  "text": "دی"
                },
                {
                  "value": "11",
                  "text": "بهمن"
                },
                {
                  "value": "12",
                  "text": "اسفند"
                }
              ]
            },
            {
              "type": "radiogroup",
              "name": "clinical_examination_result",
              "title": "نتیجه معاینه چه بوده است؟",
              "visibleIf": "{clinical_examination_history} = true",
              "isRequired": true,
              "choices": [
                {
                  "value": "1",
                  "text": "طبیعی"
                },
                {
                  "value": "2",
                  "text": "غیر طبیعی"
                }
              ]
            }
          ]
        },
        {
          "type": "panel",
          "name": "panel14",
          "elements": [
            {
              "type": "radiogroup",
              "name": "mammography_history",
              "title": "آیا تاکنون ماموگرافی انجام داده اید؟",
              "isRequired": true,
              "choices": [
                {
                  "value": "false",
                  "text": "خیر"
                },
                {
                  "value": "true",
                  "text": "بله"
                }
              ]
            },
            {
              "type": "text",
              "name": "mammography_count",
              "visibleIf": "{mammography_history} = true",
              "title": "چند نوبت؟",
              "isRequired": true,
              "inputType": "number"
            },
            {
              "type": "text",
              "name": "question14_1_year",
              "visibleIf": "{question14} = true",
              "title": "سال",
              "isRequired": true,
              "inputType": "number",
              "min": 1300,
              "max": 1402,
              "minErrorText": "حداقل مقدار سال 1300 است",
              "maxErrorText": "حداکثر مقدار سال 1402 است"
            },
            {
              "type": "dropdown",
              "name": "question14_1_month",
              "visibleIf": "{question14} = true",
              "startWithNewLine": false,
              "title": "ماه",
              "isRequired": true,
              "choices": [
                {
                  "value": "01",
                  "text": "فروردین"
                },
                {
                  "value": "02",
                  "text": "اردیبهشت"
                },
                {
                  "value": "03",
                  "text": "خرداد"
                },
                {
                  "value": "04",
                  "text": "تیر"
                },
                {
                  "value": "05",
                  "text": "مرداد"
                },
                {
                  "value": "06",
                  "text": "شهریور"
                },
                {
                  "value": "07",
                  "text": "مهر"
                },
                {
                  "value": "08",
                  "text": "آبان"
                },
                {
                  "value": "09",
                  "text": "آذر"
                },
                {
                  "value": "10",
                  "text": "دی"
                },
                {
                  "value": "11",
                  "text": "بهمن"
                },
                {
                  "value": "12",
                  "text": "اسفند"
                }
              ]
            },
            {
              "type": "expression",
              "name": "question14_1",
              "visible": false,
              "clearIfInvisible": "none",
              "isRequired": true,
              "expression": "{question14_1_year}+\"/\"+{question14_1_month}+\"/01\""
            },
            {
              "type": "radiogroup",
              "name": "mammography_result",
              "title": "نتیجه معاینه چه بوده است؟",
              "visibleIf": "{clinical_examination_history} = true",
              "isRequired": true,
              "choices": [
                {
                  "value": "1",
                  "text": "طبیعی"
                },
                {
                  "value": "2",
                  "text": "غیر طبیعی، ضایعات خوشخیم"
                },
                {
                  "value": "2",
                  "text": "غیر طبیعی، ضایعات مشکوک به بدخیم"
                }
              ]
            }
          ]
        },
        {
          "type": "panel",
          "name": "panel15",
          "elements": [
            {
              "type": "radiogroup",
              "name": "question15",
              "title": "آیا تاکنون سونوگرافی از پستان انجام داده اید؟",
              "isRequired": true,
              "choices": [
                {
                  "value": "false",
                  "text": "خیر"
                },
                {
                  "value": "true",
                  "text": "بله"
                }
              ]
            },
            {
              "type": "text",
              "name": "question15_1_year",
              "visibleIf": "{question15} = true",
              "title": "سال",
              "isRequired": true,
              "inputType": "number",
              "min": 1300,
              "max": 1402,
              "minErrorText": "حداقل مقدار سال 1300 است",
              "maxErrorText": "حداکثر مقدار سال 1402 است"
            },
            {
              "type": "dropdown",
              "name": "question15_1_month",
              "visibleIf": "{question15} = true",
              "startWithNewLine": false,
              "title": "ماه",
              "isRequired": true,
              "choices": [
                {
                  "value": "01",
                  "text": "فروردین"
                },
                {
                  "value": "02",
                  "text": "اردیبهشت"
                },
                {
                  "value": "03",
                  "text": "خرداد"
                },
                {
                  "value": "04",
                  "text": "تیر"
                },
                {
                  "value": "05",
                  "text": "مرداد"
                },
                {
                  "value": "06",
                  "text": "شهریور"
                },
                {
                  "value": "07",
                  "text": "مهر"
                },
                {
                  "value": "08",
                  "text": "آبان"
                },
                {
                  "value": "09",
                  "text": "آذر"
                },
                {
                  "value": "10",
                  "text": "دی"
                },
                {
                  "value": "11",
                  "text": "بهمن"
                },
                {
                  "value": "12",
                  "text": "اسفند"
                }
              ]
            },
            {
              "type": "expression",
              "name": "question15_1",
              "visible": false,
              "clearIfInvisible": "none",
              "isRequired": true,
              "expression": "{question15_1_year}+\"/\"+{question15_1_month}+\"/01\""
            }
          ]
        },
        {
          "type": "panel",
          "name": "panel5",
          "elements": [
            {
              "type": "radiogroup",
              "name": "question5",
              "title": "آیا سابقه نمونه برداری از پستان دارید؟",
              "isRequired": true,
              "choices": [
                {
                  "value": "false",
                  "text": "ندارم"
                },
                {
                  "value": "true",
                  "text": "دارم"
                }
              ]
            },
            {
              "type": "text",
              "name": "question5_1_year",
              "visibleIf": "{question5} = true",
              "title": "سال",
              "isRequired": true,
              "inputType": "number",
              "min": 1300,
              "max": 1402,
              "minErrorText": "حداقل مقدار سال 1300 است",
              "maxErrorText": "حداکثر مقدار سال 1402 است"
            },
            {
              "type": "dropdown",
              "name": "question5_1_month",
              "visibleIf": "{question5} = true",
              "startWithNewLine": false,
              "title": "ماه",
              "isRequired": true,
              "choices": [
                {
                  "value": "01",
                  "text": "فروردین"
                },
                {
                  "value": "02",
                  "text": "اردیبهشت"
                },
                {
                  "value": "03",
                  "text": "خرداد"
                },
                {
                  "value": "04",
                  "text": "تیر"
                },
                {
                  "value": "05",
                  "text": "مرداد"
                },
                {
                  "value": "06",
                  "text": "شهریور"
                },
                {
                  "value": "07",
                  "text": "مهر"
                },
                {
                  "value": "08",
                  "text": "آبان"
                },
                {
                  "value": "09",
                  "text": "آذر"
                },
                {
                  "value": "10",
                  "text": "دی"
                },
                {
                  "value": "11",
                  "text": "بهمن"
                },
                {
                  "value": "12",
                  "text": "اسفند"
                }
              ]
            },
            {
              "type": "expression",
              "name": "question5_1",
              "visible": false,
              "clearIfInvisible": "none",
              "isRequired": true,
              "expression": "{question5_1_year}+\"/\"+{question5_1_month}+\"/01\""
            },
            {
              "type": "radiogroup",
              "name": "question5_2",
              "visibleIf": "{question5} = true",
              "title": "نتیجه نمونه برداری؟",
              "isRequired": true,
              "choices": [
                {
                  "value": "lab_result_ala",
                  "text": "پاسخ آزمایش LCIS، ALH یا ADH بوده است"
                },
                {
                  "value": "lab_result_other",
                  "text": "پاسخ آزمایش به جز سه مورد گزینه قبلی بوده است"
                },
                {
                  "value": "lab_result_dont_know",
                  "text": "پاسخ آزمایش را نمی دانم"
                }
              ]
            }
          ]
        },
        {
          "type": "panel",
          "name": "panel20",
          "elements": [
            {
              "type": "radiogroup",
              "name": "question20",
              "title": "آیا جهش در ژن های BRCA1 یا BRCA 2 دارید؟",
              "isRequired": true,
              "choices": [
                {
                  "value": "1",
                  "text": "تا کنون این تست را انجام نداده ام"
                },
                {
                  "value": "2",
                  "text": "این تست را انجام داده ام و نتیجه آن منفی بوده"
                },
                {
                  "value": "3",
                  "text": "این تست را انجام داده ام و نتیجه آن مثبت (جهش در یکی از این ژن ها) بوده است"
                },
                {
                  "value": "4",
                  "text": "نمی دانم"
                }
              ]
            }
          ]
        },
        {
          "type": "panel",
          "name": "panel6",
          "elements": [
            {
              "type": "radiogroup",
              "name": "question6",
              "title": "آیا سابقه رادیوتراپی (پرتودرمانی) قفسه سینه دارید؟",
              "isRequired": true,
              "choices": [
                {
                  "value": "false",
                  "text": "ندارم"
                },
                {
                  "value": "true",
                  "text": "دارم"
                }
              ]
            },
            {
              "type": "text",
              "name": "question6_1_year",
              "visibleIf": "{question6} = true",
              "title": "سال",
              "isRequired": true,
              "inputType": "number",
              "min": 1300,
              "max": 1402,
              "minErrorText": "حداقل مقدار سال 1300 است",
              "maxErrorText": "حداکثر مقدار سال 1402 است"
            },
            {
              "type": "dropdown",
              "name": "question6_1_month",
              "visibleIf": "{question6} = true",
              "startWithNewLine": false,
              "title": "ماه",
              "isRequired": true,
              "choices": [
                {
                  "value": "01",
                  "text": "فروردین"
                },
                {
                  "value": "02",
                  "text": "اردیبهشت"
                },
                {
                  "value": "03",
                  "text": "خرداد"
                },
                {
                  "value": "04",
                  "text": "تیر"
                },
                {
                  "value": "05",
                  "text": "مرداد"
                },
                {
                  "value": "06",
                  "text": "شهریور"
                },
                {
                  "value": "07",
                  "text": "مهر"
                },
                {
                  "value": "08",
                  "text": "آبان"
                },
                {
                  "value": "09",
                  "text": "آذر"
                },
                {
                  "value": "10",
                  "text": "دی"
                },
                {
                  "value": "11",
                  "text": "بهمن"
                },
                {
                  "value": "12",
                  "text": "اسفند"
                }
              ]
            },
            {
              "type": "expression",
              "name": "question6_1",
              "visible": false,
              "clearIfInvisible": "none",
              "isRequired": true,
              "expression": "{question6_1_year}+\"/\"+{question6_1_month}+\"/01\""
            }
          ]
        },
        {
          "type": "panel",
          "name": "panel7",
          "elements": [
            {
              "type": "radiogroup",
              "name": "question7",
              "title": "آیا شما در گذشته سابقه ابتلا به بیماری سرطان پستان، تخمدان یا پانکراس (لوزالمعده) داشته اید؟",
              "isRequired": true,
              "choices": [
                {
                  "value": "false",
                  "text": "نداشته ام "
                },
                {
                  "value": "true",
                  "text": "داشته ام "
                }
              ]
            },
            {
              "type": "radiogroup",
              "name": "question7_1",
              "visibleIf": "{question7} = true",
              "title": "سابقه ابتلاء به سرطان پستان",
              "isRequired": true,
              "validators": [
                {
                  "type": "expression",
                  "text": "حداقل یکی از سوابق میبایست تکمیل گردد",
                  "expression": "{question7_1} <> false or {question7_2} <> false or {question7_3} <> false  or {question7_4} <> false"
                }
              ],
              "choices": [
                {
                  "value": "false",
                  "text": "نداشته ام"
                },
                {
                  "value": "oneSide",
                  "text": "یک طرفه"
                },
                {
                  "value": "twoSide",
                  "text": "دو طرفه"
                }
              ]
            },
            {
              "type": "text",
              "name": "question7_1_1_year",
              "visibleIf": "{question7} = true and {question7_1} = 'oneSide'",
              "title": "سال ابتلا",
              "isRequired": true,
              "inputType": "number",
              "min": 1300,
              "max": 1402,
              "minErrorText": "حداقل مقدار سال 1300 است",
              "maxErrorText": "حداکثر مقدار سال 1402 است"
            },
            {
              "type": "dropdown",
              "name": "question7_1_1_month",
              "visibleIf": "{question7} = true and {question7_1} = 'oneSide'",
              "startWithNewLine": false,
              "title": "ماه ابتلا",
              "isRequired": true,
              "choices": [
                {
                  "value": "01",
                  "text": "فروردین"
                },
                {
                  "value": "02",
                  "text": "اردیبهشت"
                },
                {
                  "value": "03",
                  "text": "خرداد"
                },
                {
                  "value": "04",
                  "text": "تیر"
                },
                {
                  "value": "05",
                  "text": "مرداد"
                },
                {
                  "value": "06",
                  "text": "شهریور"
                },
                {
                  "value": "07",
                  "text": "مهر"
                },
                {
                  "value": "08",
                  "text": "آبان"
                },
                {
                  "value": "09",
                  "text": "آذر"
                },
                {
                  "value": "10",
                  "text": "دی"
                },
                {
                  "value": "11",
                  "text": "بهمن"
                },
                {
                  "value": "12",
                  "text": "اسفند"
                }
              ]
            },
            {
              "type": "expression",
              "name": "question7_1_1",
              "visible": false,
              "clearIfInvisible": "none",
              "isRequired": true,
              "expression": "{question7_1_1_year}+\"/\"+{question7_1_1_month}+\"/01\""
            },
            {
              "type": "text",
              "name": "question7_1_2_year",
              "visibleIf": "{question7} = true and {question7_1} = 'twoSide'",
              "title": "سال ابتلا (پستان چپ)",
              "isRequired": true,
              "inputType": "number",
              "min": 1300,
              "max": 1402,
              "minErrorText": "حداقل مقدار سال 1300 است",
              "maxErrorText": "حداکثر مقدار سال 1402 است"
            },
            {
              "type": "dropdown",
              "name": "question7_1_2_month",
              "visibleIf": "{question7} = true and {question7_1} = 'twoSide'",
              "startWithNewLine": false,
              "title": "ماه ابتلا (پستان چپ)",
              "isRequired": true,
              "choices": [
                {
                  "value": "01",
                  "text": "فروردین"
                },
                {
                  "value": "02",
                  "text": "اردیبهشت"
                },
                {
                  "value": "03",
                  "text": "خرداد"
                },
                {
                  "value": "04",
                  "text": "تیر"
                },
                {
                  "value": "05",
                  "text": "مرداد"
                },
                {
                  "value": "06",
                  "text": "شهریور"
                },
                {
                  "value": "07",
                  "text": "مهر"
                },
                {
                  "value": "08",
                  "text": "آبان"
                },
                {
                  "value": "09",
                  "text": "آذر"
                },
                {
                  "value": "10",
                  "text": "دی"
                },
                {
                  "value": "11",
                  "text": "بهمن"
                },
                {
                  "value": "12",
                  "text": "اسفند"
                }
              ]
            },
            {
              "type": "expression",
              "name": "question7_1_2",
              "visible": false,
              "clearIfInvisible": "none",
              "isRequired": true,
              "expression": "{question7_1_2_year}+\"/\"+{question7_1_2_month}+\"/01\""
            },
            {
              "type": "text",
              "name": "question7_1_3_year",
              "visibleIf": "{question7} = true and {question7_1} = 'twoSide'",
              "title": "سال ابتلا (پستان راست)",
              "isRequired": true,
              "inputType": "number",
              "min": 1300,
              "max": 1402,
              "minErrorText": "حداقل مقدار سال 1300 است",
              "maxErrorText": "حداکثر مقدار سال 1402 است"
            },
            {
              "type": "dropdown",
              "name": "question7_1_3_month",
              "visibleIf": "{question7} = true and {question7_1} = 'twoSide'",
              "startWithNewLine": false,
              "title": "ماه ابتلا (پستان راست)",
              "isRequired": true,
              "choices": [
                {
                  "value": "01",
                  "text": "فروردین"
                },
                {
                  "value": "02",
                  "text": "اردیبهشت"
                },
                {
                  "value": "03",
                  "text": "خرداد"
                },
                {
                  "value": "04",
                  "text": "تیر"
                },
                {
                  "value": "05",
                  "text": "مرداد"
                },
                {
                  "value": "06",
                  "text": "شهریور"
                },
                {
                  "value": "07",
                  "text": "مهر"
                },
                {
                  "value": "08",
                  "text": "آبان"
                },
                {
                  "value": "09",
                  "text": "آذر"
                },
                {
                  "value": "10",
                  "text": "دی"
                },
                {
                  "value": "11",
                  "text": "بهمن"
                },
                {
                  "value": "12",
                  "text": "اسفند"
                }
              ]
            },
            {
              "type": "expression",
              "name": "question7_1_3",
              "visible": false,
              "clearIfInvisible": "none",
              "isRequired": true,
              "expression": "{question7_1_3_year}+\"/\"+{question7_1_3_month}+\"/01\""
            },
            {
              "type": "radiogroup",
              "name": "question7_2",
              "visibleIf": "{question7} = true",
              "title": "سابقه ابتلاء به سرطان تخمدان",
              "isRequired": true,
              "validators": [
                {
                  "type": "expression",
                  "text": "حداقل یکی از سوابق میبایست تکمیل گردد",
                  "expression": "{question7_1} <> false or {question7_2} <> false or {question7_3} <> false  or {question7_4} <> false"
                }
              ],
              "choices": [
                {
                  "value": "false",
                  "text": "نداشته ام "
                },
                {
                  "value": "true",
                  "text": "داشته ام "
                }
              ]
            },
            {
              "type": "text",
              "name": "question7_2_1_year",
              "visibleIf": "{question7} = true and {question7_2} = true",
              "title": "سال ابتلا",
              "isRequired": true,
              "inputType": "number",
              "min": 1300,
              "max": 1402,
              "minErrorText": "حداقل مقدار سال 1300 است",
              "maxErrorText": "حداکثر مقدار سال 1402 است"
            },
            {
              "type": "dropdown",
              "name": "question7_2_1_month",
              "visibleIf": "{question7} = true and {question7_2} = true",
              "startWithNewLine": false,
              "title": "ماه ابتلا",
              "isRequired": true,
              "choices": [
                {
                  "value": "01",
                  "text": "فروردین"
                },
                {
                  "value": "02",
                  "text": "اردیبهشت"
                },
                {
                  "value": "03",
                  "text": "خرداد"
                },
                {
                  "value": "04",
                  "text": "تیر"
                },
                {
                  "value": "05",
                  "text": "مرداد"
                },
                {
                  "value": "06",
                  "text": "شهریور"
                },
                {
                  "value": "07",
                  "text": "مهر"
                },
                {
                  "value": "08",
                  "text": "آبان"
                },
                {
                  "value": "09",
                  "text": "آذر"
                },
                {
                  "value": "10",
                  "text": "دی"
                },
                {
                  "value": "11",
                  "text": "بهمن"
                },
                {
                  "value": "12",
                  "text": "اسفند"
                }
              ]
            },
            {
              "type": "expression",
              "name": "question7_2_1",
              "visible": false,
              "clearIfInvisible": "none",
              "isRequired": true,
              "expression": "{question7_2_1_year}+\"/\"+{question7_2_1_month}+\"/01\""
            },
            {
              "type": "radiogroup",
              "name": "question7_3",
              "visibleIf": "{question7} = true",
              "title": "سابقه ابتلاء به سرطان پانکراس (لوزالمعده)",
              "isRequired": true,
              "validators": [
                {
                  "type": "expression",
                  "text": "حداقل یکی از سوابق میبایست تکمیل گردد",
                  "expression": "{question7_1} <> false or {question7_2} <> false or {question7_3} <> false  or {question7_4} <> false"
                }
              ],
              "choices": [
                {
                  "value": "false",
                  "text": "نداشته ام "
                },
                {
                  "value": "true",
                  "text": "داشته ام "
                }
              ]
            },
            {
              "type": "text",
              "name": "question7_3_1_year",
              "visibleIf": "{question7} = true and {question7_3} = true",
              "title": "سال ابتلا",
              "isRequired": true,
              "inputType": "number",
              "min": 1300,
              "max": 1402,
              "minErrorText": "حداقل مقدار سال 1300 است",
              "maxErrorText": "حداکثر مقدار سال 1402 است"
            },
            {
              "type": "dropdown",
              "name": "question7_3_1_month",
              "visibleIf": "{question7} = true and {question7_3} = true",
              "startWithNewLine": false,
              "title": "ماه ابتلا",
              "isRequired": true,
              "choices": [
                {
                  "value": "01",
                  "text": "فروردین"
                },
                {
                  "value": "02",
                  "text": "اردیبهشت"
                },
                {
                  "value": "03",
                  "text": "خرداد"
                },
                {
                  "value": "04",
                  "text": "تیر"
                },
                {
                  "value": "05",
                  "text": "مرداد"
                },
                {
                  "value": "06",
                  "text": "شهریور"
                },
                {
                  "value": "07",
                  "text": "مهر"
                },
                {
                  "value": "08",
                  "text": "آبان"
                },
                {
                  "value": "09",
                  "text": "آذر"
                },
                {
                  "value": "10",
                  "text": "دی"
                },
                {
                  "value": "11",
                  "text": "بهمن"
                },
                {
                  "value": "12",
                  "text": "اسفند"
                }
              ]
            },
            {
              "type": "expression",
              "name": "question7_3_1",
              "visible": false,
              "clearIfInvisible": "none",
              "isRequired": true,
              "expression": "{question7_3_1_year}+\"/\"+{question7_3_1_month}+\"/01\""
            },
            {
              "type": "radiogroup",
              "name": "question7_4",
              "visibleIf": "{question7} = true",
              "title": "سابقه ابتلاء به سرطان های دیگر",
              "isRequired": true,
              "validators": [
                {
                  "type": "expression",
                  "text": "حداقل یکی از سوابق میبایست تکمیل گردد",
                  "expression": "{question7_1} <> false or {question7_2} <> false or {question7_3} <> false  or {question7_4} <> false"
                }
              ],
              "choices": [
                {
                  "value": "false",
                  "text": "نداشته ام "
                },
                {
                  "value": "true",
                  "text": "داشته ام "
                }
              ]
            },
            {
              "type": "text",
              "name": "question7_4_1_year",
              "visibleIf": "{question7} = true and {question7_4} = true",
              "title": "سال ابتلا",
              "isRequired": true,
              "inputType": "number",
              "min": 1300,
              "max": 1402,
              "minErrorText": "حداقل مقدار سال 1300 است",
              "maxErrorText": "حداکثر مقدار سال 1402 است"
            },
            {
              "type": "dropdown",
              "name": "question7_4_1_month",
              "visibleIf": "{question7} = true and {question7_4} = true",
              "startWithNewLine": false,
              "title": "ماه ابتلا",
              "isRequired": true,
              "choices": [
                {
                  "value": "01",
                  "text": "فروردین"
                },
                {
                  "value": "02",
                  "text": "اردیبهشت"
                },
                {
                  "value": "03",
                  "text": "خرداد"
                },
                {
                  "value": "04",
                  "text": "تیر"
                },
                {
                  "value": "05",
                  "text": "مرداد"
                },
                {
                  "value": "06",
                  "text": "شهریور"
                },
                {
                  "value": "07",
                  "text": "مهر"
                },
                {
                  "value": "08",
                  "text": "آبان"
                },
                {
                  "value": "09",
                  "text": "آذر"
                },
                {
                  "value": "10",
                  "text": "دی"
                },
                {
                  "value": "11",
                  "text": "بهمن"
                },
                {
                  "value": "12",
                  "text": "اسفند"
                }
              ]
            },
            {
              "type": "expression",
              "name": "question7_4_1",
              "visible": false,
              "clearIfInvisible": "none",
              "isRequired": true,
              "expression": "{question7_4_1_year}+\"/\"+{question7_4_1_month}+\"/01\""
            }
          ]
        }
      ]
    },
    {
      "name": "page3",
      "title": "سوابق خانوادگی",
      "elements": [
        {
          "type": "panel",
          "name": "panel_8",
          "elements": [
            {
              "type": "radiogroup",
              "name": "question8",
              "title": "آیا در خانواده شما سابقه ابتلا به سرطان پستان، تخمدان، پروستات یا پانکراس وجود دارد؟",
              "isRequired": true,
              "choices": [
                {
                  "value": "false",
                  "text": "ندارد"
                },
                {
                  "value": "true",
                  "text": "دارد"
                }
              ]
            }
          ]
        },
        {
          "type": "panel",
          "name": "panel_8_1",
          "visibleIf": "{question8} = true",
          "elements": [
            {
              "type": "radiogroup",
              "name": "question8_1",
              "title": "سابقه ابتلا به سرطان پستان در خانواده",
              "isRequired": true,
              "validators": [
                {
                  "type": "expression",
                  "text": "حداقل یکی از سوابق میبایست تکمیل گردد",
                  "expression": "{question8_1} <> false or {question8_2} <> false or {question8_3} <> false or {question8_4} <> false or {question8_5} <> false  or {question8_6} <> false"
                }
              ],
              "choices": [
                {
                  "value": "false",
                  "text": "خیر"
                },
                {
                  "value": "true",
                  "text": "بلی"
                }
              ]
            },
            {
              "type": "paneldynamic",
              "name": "panelQ8_1",
              "visibleIf": "{question8} = true and {question8_1} = true",
              "title": "اطلاعات فرد مبتلا",
              "templateElements": [
                {
                  "type": "radiogroup",
                  "name": "question8_1_0",
                  "title": "سابقه ابتلا به سرطان پستان در خانواده",
                  "isRequired": true,
                  "choices": [
                    {
                      "value": "oneSide",
                      "text": "یکطرفه"
                    },
                    {
                      "value": "twoSide",
                      "text": "دوطرفه"
                    }
                  ]
                },
                {
                  "type": "dropdown",
                  "name": "question8_1_4",
                  "title": "درجه فامیلی",
                  "isRequired": true,
                  "choices": [
                    {
                      "value": "t1",
                      "text": "درجه 1(مادر، خواهر، دختر)"
                    },
                    {
                      "value": "t2",
                      "text": "درجه 2(خاله، عمه، مادربزرگ)"
                    },
                    {
                      "value": "t3",
                      "text": "درجه 3(دخترخاله، دختردایی، دخترعمه، دخترعمو)"
                    }
                  ]
                },
                {
                  "type": "dropdown",
                  "name": "question8_1_5",
                  "visibleIf": "{panel.question8_1_4} = 't1'",
                  "title": "نسبت فامیلی",
                  "isRequired": true,
                  "choices": [
                    {
                      "value": "t1_1",
                      "text": "مادر"
                    },
                    {
                      "value": "t1_3",
                      "text": "خواهر"
                    },
                    {
                      "value": "t1_5",
                      "text": "دختر"
                    }
                  ]
                },
                {
                  "type": "dropdown",
                  "name": "question8_1_5_t2",
                  "visibleIf": "{panel.question8_1_4} = 't2'",
                  "title": "نسبت فامیلی",
                  "isRequired": true,
                  "choices": [
                    {
                      "value": "t2_1",
                      "text": "خاله"
                    },
                    {
                      "value": "t2_3",
                      "text": "عمه"
                    },
                    {
                      "value": "t2_5",
                      "text": "مادربزرگ(مادری)"
                    },
                    {
                      "value": "t2_7",
                      "text": "مادربزرگ(پدری)"
                    }
                  ]
                },
                {
                  "type": "dropdown",
                  "name": "question8_1_5_t3",
                  "visibleIf": "{panel.question8_1_4} = 't3'",
                  "title": "نسبت فامیلی",
                  "isRequired": true,
                  "choices": [
                    {
                      "value": "t3_1",
                      "text": "دخترخاله"
                    },
                    {
                      "value": "t3_3",
                      "text": "دختردایی"
                    },
                    {
                      "value": "t3_5",
                      "text": "دخترعمه"
                    },
                    {
                      "value": "t3_7",
                      "text": "دخترعمو"
                    }
                  ]
                },
                {
                  "type": "text",
                  "name": "question8_1_6",
                  "visibleIf": "{panel.question8_1_0} = 'twoSide'",
                  "title": "سن ابتلاء به سرطان پستان راست",
                  "isRequired": true,
                  "inputType": "number",
                  "min": 25,
                  "max": 120,
                  "minErrorText": "حداقل مقدار قابل قبول 25 است",
                  "maxErrorText": "حداکثر مقدار قابل قبول 120 است"
                },
                {
                  "type": "text",
                  "name": "question8_1_6_year",
                  "visibleIf": "{panel.question8_1_0} = 'twoSide'",
                  "startWithNewLine": false,
                  "title": "سال تولد",
                  "isRequired": true,
                  "inputType": "number",
                  "min": 1300,
                  "max": 1402,
                  "minErrorText": "حداقل مقدار سال 1300 است",
                  "maxErrorText": "حداکثر مقدار سال 1402 است"
                },
                {
                  "type": "text",
                  "name": "question8_1_7",
                  "visibleIf": "{panel.question8_1_0} = 'twoSide'",
                  "title": "سن ابتلاء به سرطان پستان چپ",
                  "isRequired": true,
                  "inputType": "number",
                  "min": 25,
                  "max": 120,
                  "minErrorText": "حداقل مقدار قابل قبول 25 است",
                  "maxErrorText": "حداکثر مقدار قابل قبول 120 است"
                },
                {
                  "type": "text",
                  "name": "question8_1_7_year",
                  "visibleIf": "{panel.question8_1_0} = 'twoSide'",
                  "startWithNewLine": false,
                  "title": "سال تولد",
                  "isRequired": true,
                  "inputType": "number",
                  "min": 1300,
                  "max": 1402,
                  "minErrorText": "حداقل مقدار سال 1300 است",
                  "maxErrorText": "حداکثر مقدار سال 1402 است"
                },
                {
                  "type": "text",
                  "name": "question8_1_8",
                  "visibleIf": "{panel.question8_1_0} = 'oneSide'",
                  "title": "سن ابتلاء به سرطان پستان",
                  "isRequired": true,
                  "inputType": "number",
                  "min": 25,
                  "max": 120,
                  "minErrorText": "حداقل مقدار قابل قبول 25 است",
                  "maxErrorText": "حداکثر مقدار قابل قبول 120 است"
                },
                {
                  "type": "text",
                  "name": "question8_1_8_year",
                  "visibleIf": "{panel.question8_1_0} = 'oneSide'",
                  "startWithNewLine": false,
                  "title": "سال تولد",
                  "isRequired": true,
                  "inputType": "number",
                  "min": 1300,
                  "max": 1402,
                  "minErrorText": "حداقل مقدار سال 1300 است",
                  "maxErrorText": "حداکثر مقدار سال 1402 است"
                }
              ],
              "panelCount": 1,
              "minPanelCount": 1,
              "maxPanelCount": 10,
              "confirmDelete": true,
              "panelAddText": "افزودن فرد مبتلا دیگر",
              "panelRemoveText": "حذف",
              "panelPrevText": "قبلی",
              "panelNextText": "بعدی"
            }
          ]
        },
        {
          "type": "panel",
          "name": "panel_8_2",
          "visibleIf": "{question8} = true",
          "elements": [
            {
              "type": "radiogroup",
              "name": "question8_2",
              "title": "سابقه ابتلا به سرطان تخمدان در خانواده",
              "isRequired": true,
              "validators": [
                {
                  "type": "expression",
                  "text": "حداقل یکی از سوابق میبایست تکمیل گردد",
                  "expression": "{question8_1} <> false or {question8_2} <> false or {question8_3} <> false or {question8_4} <> false or {question8_5} <> false  or {question8_6} <> false"
                }
              ],
              "choices": [
                {
                  "value": "false",
                  "text": "خیر"
                },
                {
                  "value": "true",
                  "text": "بلی"
                }
              ]
            },
            {
              "type": "paneldynamic",
              "name": "panelQ8_2",
              "visibleIf": "{question8} = true and {question8_2} = true",
              "title": "اطلاعات فرد مبتلا",
              "templateElements": [
                {
                  "type": "dropdown",
                  "name": "question8_2_1",
                  "title": "درجه فامیلی",
                  "isRequired": true,
                  "choices": [
                    {
                      "value": "t1",
                      "text": "درجه 1(مادر، خواهر، دختر)"
                    },
                    {
                      "value": "t2",
                      "text": "درجه 2(خاله، عمه، مادربزرگ)"
                    },
                    {
                      "value": "t3",
                      "text": "درجه 3(دخترخاله، دختردایی، دخترعمه، دخترعمو)"
                    }
                  ]
                },
                {
                  "type": "dropdown",
                  "name": "question8_2_2",
                  "visibleIf": "{panel.question8_2_1} = 't1'",
                  "title": "نسبت فامیلی",
                  "isRequired": true,
                  "choices": [
                    {
                      "value": "t1_1",
                      "text": "مادر"
                    },
                    {
                      "value": "t1_3",
                      "text": "خواهر"
                    },
                    {
                      "value": "t1_5",
                      "text": "دختر"
                    }
                  ]
                },
                {
                  "type": "dropdown",
                  "name": "question8_2_2_t2",
                  "visibleIf": "{panel.question8_2_1} = 't2'",
                  "title": "نسبت فامیلی",
                  "isRequired": true,
                  "choices": [
                    {
                      "value": "t2_1",
                      "text": "خاله"
                    },
                    {
                      "value": "t2_3",
                      "text": "عمه"
                    },
                    {
                      "value": "t2_5",
                      "text": "مادربزرگ(مادری)"
                    },
                    {
                      "value": "t2_7",
                      "text": "مادربزرگ(پدری)"
                    }
                  ]
                },
                {
                  "type": "dropdown",
                  "name": "question8_2_2_t3",
                  "visibleIf": "{panel.question8_2_1} = 't3'",
                  "title": "نسبت فامیلی",
                  "isRequired": true,
                  "choices": [
                    {
                      "value": "t3_1",
                      "text": "دخترخاله"
                    },
                    {
                      "value": "t3_3",
                      "text": "دختردایی"
                    },
                    {
                      "value": "t3_5",
                      "text": "دخترعمه"
                    },
                    {
                      "value": "t3_7",
                      "text": "دخترعمو"
                    }
                  ]
                },
                {
                  "type": "text",
                  "name": "question8_2_3",
                  "title": "سن ابتلاء به سرطان پستان",
                  "isRequired": true,
                  "inputType": "number",
                  "min": 25,
                  "max": 120,
                  "minErrorText": "حداقل مقدار قابل قبول 25 است",
                  "maxErrorText": "حداکثر مقدار قابل قبول 120 است"
                },
                {
                  "type": "text",
                  "name": "question8_2_3_year",
                  "startWithNewLine": false,
                  "title": "سال تولد",
                  "isRequired": true,
                  "inputType": "number",
                  "min": 1300,
                  "max": 1402,
                  "minErrorText": "حداقل مقدار سال 1300 است",
                  "maxErrorText": "حداکثر مقدار سال 1402 است"
                }
              ],
              "panelCount": 1,
              "minPanelCount": 1,
              "maxPanelCount": 10,
              "confirmDelete": true,
              "panelAddText": "افزودن فرد مبتلا دیگر",
              "panelRemoveText": "حذف",
              "panelPrevText": "قبلی",
              "panelNextText": "بعدی"
            }
          ]
        },
        {
          "type": "panel",
          "name": "panel_8_3",
          "visibleIf": "{question8} = true",
          "elements": [
            {
              "type": "radiogroup",
              "name": "question8_3",
              "title": "سابقه ابتلا به سرطان پانکراس در خانواده",
              "isRequired": true,
              "validators": [
                {
                  "type": "expression",
                  "text": "حداقل یکی از سوابق میبایست تکمیل گردد",
                  "expression": "{question8_1} <> false or {question8_2} <> false or {question8_3} <> false or {question8_4} <> false or {question8_5} <> false  or {question8_6} <> false"
                }
              ],
              "choices": [
                {
                  "value": "false",
                  "text": "خیر"
                },
                {
                  "value": "true",
                  "text": "بلی"
                }
              ]
            },
            {
              "type": "paneldynamic",
              "name": "panelQ8_3",
              "visibleIf": "{question8} = true and {question8_3} = true",
              "title": "اطلاعات فرد مبتلا",
              "templateElements": [
                {
                  "type": "dropdown",
                  "name": "question8_3_1",
                  "title": "درجه فامیلی",
                  "isRequired": true,
                  "choices": [
                    {
                      "value": "t1",
                      "text": "درجه 1(مادر، پدر، خواهر، برادر، دختر، پسر)"
                    },
                    {
                      "value": "t2",
                      "text": "درجه 2(خاله، دایی، عمه، عمو، مادربزرگ، پدربزرگ)"
                    },
                    {
                      "value": "t3",
                      "text": "درجه 3(دخترخاله، پسرخاله، دختردایی، پسردایی، دخترعمه، پسرعمه، دخترعمو، پسرعمو)"
                    }
                  ]
                },
                {
                  "type": "dropdown",
                  "name": "question8_3_2",
                  "visibleIf": "{panel.question8_3_1} = 't1'",
                  "title": "نسبت فامیلی",
                  "isRequired": true,
                  "choices": [
                    {
                      "value": "t1_1",
                      "text": "مادر"
                    },
                    {
                      "value": "t1_2",
                      "text": "پدر"
                    },
                    {
                      "value": "t1_3",
                      "text": "خواهر"
                    },
                    {
                      "value": "t1_4",
                      "text": "برادر"
                    },
                    {
                      "value": "t1_5",
                      "text": "دختر"
                    },
                    {
                      "value": "t1_6",
                      "text": "پسر"
                    }
                  ]
                },
                {
                  "type": "dropdown",
                  "name": "question8_3_2_t2",
                  "visibleIf": "{panel.question8_3_1} = 't2'",
                  "title": "نسبت فامیلی",
                  "isRequired": true,
                  "choices": [
                    {
                      "value": "t2_1",
                      "text": "خاله"
                    },
                    {
                      "value": "t2_2",
                      "text": "دایی"
                    },
                    {
                      "value": "t2_3",
                      "text": "عمه"
                    },
                    {
                      "value": "t2_4",
                      "text": "عمو"
                    },
                    {
                      "value": "t2_5",
                      "text": "مادربزرگ(مادری)"
                    },
                    {
                      "value": "t2_6",
                      "text": "پدربزرگ(مادری)"
                    },
                    {
                      "value": "t2_7",
                      "text": "مادربزرگ(پدری)"
                    },
                    {
                      "value": "t2_8",
                      "text": "پدربزرگ(پدری)"
                    }
                  ]
                },
                {
                  "type": "dropdown",
                  "name": "question8_3_2_t3",
                  "visibleIf": "{panel.question8_3_1} = 't3'",
                  "title": "نسبت فامیلی",
                  "isRequired": true,
                  "choices": [
                    {
                      "value": "t3_1",
                      "text": "دخترخاله"
                    },
                    {
                      "value": "t3_2",
                      "text": "پسرخاله"
                    },
                    {
                      "value": "t3_3",
                      "text": "دختردایی"
                    },
                    {
                      "value": "t3_4",
                      "text": "پسردایی"
                    },
                    {
                      "value": "t3_5",
                      "text": "دخترعمه"
                    },
                    {
                      "value": "t3_6",
                      "text": "پسرعمه"
                    },
                    {
                      "value": "t3_7",
                      "text": "دخترعمو"
                    },
                    {
                      "value": "t3_8",
                      "text": "پسرعمو"
                    }
                  ]
                },
                {
                  "type": "text",
                  "name": "question8_3_3",
                  "title": "سن ابتلا",
                  "isRequired": true,
                  "inputType": "number",
                  "min": 25,
                  "max": 120,
                  "minErrorText": "حداقل مقدار قابل قبول 25 است",
                  "maxErrorText": "حداکثر مقدار قابل قبول 120 است"
                },
                {
                  "type": "text",
                  "name": "question8_3_3_year",
                  "startWithNewLine": false,
                  "title": "سال تولد",
                  "isRequired": true,
                  "inputType": "number",
                  "min": 1300,
                  "max": 1402,
                  "minErrorText": "حداقل مقدار سال 1300 است",
                  "maxErrorText": "حداکثر مقدار سال 1402 است"
                }
              ],
              "panelCount": 1,
              "minPanelCount": 1,
              "maxPanelCount": 10,
              "confirmDelete": true,
              "panelAddText": "افزودن فرد مبتلا دیگر",
              "panelRemoveText": "حذف",
              "panelPrevText": "قبلی",
              "panelNextText": "بعدی"
            }
          ]
        },
        {
          "type": "panel",
          "name": "panel_8_4",
          "visibleIf": "{question8} = true",
          "elements": [
            {
              "type": "radiogroup",
              "name": "question8_4",
              "title": "سابقه ابتلا به سرطان پروستات در خانواده",
              "isRequired": true,
              "validators": [
                {
                  "type": "expression",
                  "text": "حداقل یکی از سوابق میبایست تکمیل گردد",
                  "expression": "{question8_1} <> false or {question8_2} <> false or {question8_3} <> false or {question8_4} <> false or {question8_5} <> false  or {question8_6} <> false"
                }
              ],
              "choices": [
                {
                  "value": "false",
                  "text": "خیر"
                },
                {
                  "value": "true",
                  "text": "بلی"
                }
              ]
            },
            {
              "type": "paneldynamic",
              "name": "panelQ8_4",
              "visibleIf": "{question8} = true and {question8_4} = true",
              "title": "اطلاعات فرد مبتلا",
              "templateElements": [
                {
                  "type": "dropdown",
                  "name": "question8_4_1",
                  "title": "درجه فامیلی",
                  "isRequired": true,
                  "choices": [
                    {
                      "value": "t1",
                      "text": "درجه 1(پدر، برادر، پسر)"
                    },
                    {
                      "value": "t2",
                      "text": "درجه 2(دایی، عمو، پدربزرگ)"
                    },
                    {
                      "value": "t3",
                      "text": "درجه 3(پسرخاله، پسردایی، پسرعمه، پسرعمو)"
                    }
                  ]
                },
                {
                  "type": "dropdown",
                  "name": "question8_4_2",
                  "visibleIf": "{panel.question8_4_1} = 't1'",
                  "title": "نسبت فامیلی",
                  "isRequired": true,
                  "choices": [
                    {
                      "value": "t1_2",
                      "text": "پدر"
                    },
                    {
                      "value": "t1_4",
                      "text": "برادر"
                    },
                    {
                      "value": "t1_6",
                      "text": "پسر"
                    }
                  ]
                },
                {
                  "type": "dropdown",
                  "name": "question8_4_2_t2",
                  "visibleIf": "{panel.question8_4_1} = 't2'",
                  "title": "نسبت فامیلی",
                  "isRequired": true,
                  "choices": [
                    {
                      "value": "t2_2",
                      "text": "دایی"
                    },
                    {
                      "value": "t2_4",
                      "text": "عمو"
                    },
                    {
                      "value": "t2_6",
                      "text": "پدربزرگ(مادری)"
                    },
                    {
                      "value": "t2_8",
                      "text": "پدربزرگ(پدری)"
                    }
                  ]
                },
                {
                  "type": "dropdown",
                  "name": "question8_4_2_t3",
                  "visibleIf": "{panel.question8_4_1} = 't3'",
                  "title": "نسبت فامیلی",
                  "isRequired": true,
                  "choices": [
                    {
                      "value": "t3_2",
                      "text": "پسرخاله"
                    },
                    {
                      "value": "t3_4",
                      "text": "پسردایی"
                    },
                    {
                      "value": "t3_6",
                      "text": "پسرعمه"
                    },
                    {
                      "value": "t3_8",
                      "text": "پسرعمو"
                    }
                  ]
                },
                {
                  "type": "text",
                  "name": "question8_4_3",
                  "title": "سن ابتلا",
                  "isRequired": true,
                  "inputType": "number",
                  "min": 25,
                  "max": 120,
                  "minErrorText": "حداقل مقدار قابل قبول 25 است",
                  "maxErrorText": "حداکثر مقدار قابل قبول 120 است"
                },
                {
                  "type": "text",
                  "name": "question8_4_3_year",
                  "startWithNewLine": false,
                  "title": "سال تولد",
                  "isRequired": true,
                  "inputType": "number",
                  "min": 1300,
                  "max": 1402,
                  "minErrorText": "حداقل مقدار سال 1300 است",
                  "maxErrorText": "حداکثر مقدار سال 1402 است"
                }
              ],
              "panelCount": 1,
              "minPanelCount": 1,
              "maxPanelCount": 10,
              "confirmDelete": true,
              "panelAddText": "افزودن فرد مبتلا دیگر",
              "panelRemoveText": "حذف",
              "panelPrevText": "قبلی",
              "panelNextText": "بعدی"
            }
          ]
        },
        {
          "type": "panel",
          "name": "panel_8_5",
          "visibleIf": "{question8} = true",
          "elements": [
            {
              "type": "radiogroup",
              "name": "question8_5",
              "title": "سابقه ابتلا به سرطان پستان در مردان خانواده",
              "isRequired": true,
              "validators": [
                {
                  "type": "expression",
                  "text": "حداقل یکی از سوابق میبایست تکمیل گردد",
                  "expression": "{question8_1} <> false or {question8_2} <> false or {question8_3} <> false or {question8_4} <> false or {question8_5} <> false  or {question8_6} <> false"
                }
              ],
              "choices": [
                {
                  "value": "false",
                  "text": "خیر"
                },
                {
                  "value": "true",
                  "text": "بلی"
                }
              ]
            },
            {
              "type": "paneldynamic",
              "name": "panelQ8_5",
              "visibleIf": "{question8} = true and {question8_5} = true",
              "title": "اطلاعات فرد مبتلا",
              "templateElements": [
                {
                  "type": "dropdown",
                  "name": "question8_5_1",
                  "title": "درجه فامیلی",
                  "isRequired": true,
                  "choices": [
                    {
                      "value": "t1",
                      "text": "درجه 1(پدر، برادر، پسر)"
                    },
                    {
                      "value": "t2",
                      "text": "درجه 2(دایی، عمو، پدربزرگ)"
                    },
                    {
                      "value": "t3",
                      "text": "درجه 3(پسرخاله، پسردایی، پسرعمه، پسرعمو)"
                    }
                  ]
                },
                {
                  "type": "dropdown",
                  "name": "question8_5_2",
                  "visibleIf": "{panel.question8_5_1} = 't1'",
                  "title": "نسبت فامیلی",
                  "isRequired": true,
                  "choices": [
                    {
                      "value": "t1_2",
                      "text": "پدر"
                    },
                    {
                      "value": "t1_4",
                      "text": "برادر"
                    },
                    {
                      "value": "t1_6",
                      "text": "پسر"
                    }
                  ]
                },
                {
                  "type": "dropdown",
                  "name": "question8_5_2_t2",
                  "visibleIf": "{panel.question8_5_1} = 't2'",
                  "title": "نسبت فامیلی",
                  "isRequired": true,
                  "choices": [
                    {
                      "value": "t2_2",
                      "text": "دایی"
                    },
                    {
                      "value": "t2_4",
                      "text": "عمو"
                    },
                    {
                      "value": "t2_6",
                      "text": "پدربزرگ(مادری)"
                    },
                    {
                      "value": "t2_8",
                      "text": "پدربزرگ(پدری)"
                    }
                  ]
                },
                {
                  "type": "dropdown",
                  "name": "question8_5_2_t3",
                  "visibleIf": "{panel.question8_5_1} = 't3'",
                  "title": "نسبت فامیلی",
                  "isRequired": true,
                  "choices": [
                    {
                      "value": "t3_2",
                      "text": "پسرخاله"
                    },
                    {
                      "value": "t3_4",
                      "text": "پسردایی"
                    },
                    {
                      "value": "t3_6",
                      "text": "پسرعمه"
                    },
                    {
                      "value": "t3_8",
                      "text": "پسرعمو"
                    }
                  ]
                },
                {
                  "type": "text",
                  "name": "question8_5_3",
                  "title": "سن ابتلا",
                  "isRequired": true,
                  "inputType": "number",
                  "min": 25,
                  "max": 120,
                  "minErrorText": "حداقل مقدار قابل قبول 25 است",
                  "maxErrorText": "حداکثر مقدار قابل قبول 120 است"
                },
                {
                  "type": "text",
                  "name": "question8_5_3_year",
                  "startWithNewLine": false,
                  "title": "سال تولد",
                  "isRequired": true,
                  "inputType": "number",
                  "min": 1300,
                  "max": 1402,
                  "minErrorText": "حداقل مقدار سال 1300 است",
                  "maxErrorText": "حداکثر مقدار سال 1402 است"
                }
              ],
              "panelCount": 1,
              "minPanelCount": 1,
              "maxPanelCount": 10,
              "confirmDelete": true,
              "panelAddText": "افزودن فرد مبتلا دیگر",
              "panelRemoveText": "حذف",
              "panelPrevText": "قبلی",
              "panelNextText": "بعدی"
            }
          ]
        },
        {
          "type": "panel",
          "name": "panel_8_6",
          "visibleIf": "{question8} = true",
          "elements": [
            {
              "type": "radiogroup",
              "name": "question8_6",
              "title": "سابقه ابتلا به سرطان های دیگر در خانواده",
              "isRequired": true,
              "validators": [
                {
                  "type": "expression",
                  "text": "حداقل یکی از سوابق میبایست تکمیل گردد",
                  "expression": "{question8_1} <> false or {question8_2} <> false or {question8_3} <> false or {question8_4} <> false or {question8_5} <> false  or {question8_6} <> false"
                }
              ],
              "choices": [
                {
                  "value": "false",
                  "text": "خیر"
                },
                {
                  "value": "true",
                  "text": "بلی"
                }
              ]
            },
            {
              "type": "paneldynamic",
              "name": "panelQ8_6",
              "visibleIf": "{question8} = true and {question8_6} = true",
              "title": "اطلاعات فرد مبتلا",
              "templateElements": [
                {
                  "type": "dropdown",
                  "name": "question8_6_1",
                  "title": "درجه فامیلی",
                  "isRequired": true,
                  "choices": [
                    {
                      "value": "t1",
                      "text": "درجه 1(پدر، برادر، پسر)"
                    },
                    {
                      "value": "t2",
                      "text": "درجه 2(دایی، عمو، پدربزرگ)"
                    },
                    {
                      "value": "t3",
                      "text": "درجه 3(پسرخاله، پسردایی، پسرعمه، پسرعمو)"
                    }
                  ]
                },
                {
                  "type": "dropdown",
                  "name": "question8_6_2",
                  "visibleIf": "{panel.question8_6_1} = 't1'",
                  "title": "نسبت فامیلی",
                  "isRequired": true,
                  "choices": [
                    {
                      "value": "t1_2",
                      "text": "پدر"
                    },
                    {
                      "value": "t1_4",
                      "text": "برادر"
                    },
                    {
                      "value": "t1_6",
                      "text": "پسر"
                    }
                  ]
                },
                {
                  "type": "dropdown",
                  "name": "question8_6_2_t2",
                  "visibleIf": "{panel.question8_6_1} = 't2'",
                  "title": "نسبت فامیلی",
                  "isRequired": true,
                  "choices": [
                    {
                      "value": "t2_2",
                      "text": "دایی"
                    },
                    {
                      "value": "t2_4",
                      "text": "عمو"
                    },
                    {
                      "value": "t2_6",
                      "text": "پدربزرگ(مادری)"
                    },
                    {
                      "value": "t2_8",
                      "text": "پدربزرگ(پدری)"
                    }
                  ]
                },
                {
                  "type": "dropdown",
                  "name": "question8_6_2_t3",
                  "visibleIf": "{panel.question8_6_1} = 't3'",
                  "title": "نسبت فامیلی",
                  "isRequired": true,
                  "choices": [
                    {
                      "value": "t3_2",
                      "text": "پسرخاله"
                    },
                    {
                      "value": "t3_4",
                      "text": "پسردایی"
                    },
                    {
                      "value": "t3_6",
                      "text": "پسرعمه"
                    },
                    {
                      "value": "t3_8",
                      "text": "پسرعمو"
                    }
                  ]
                },
                {
                  "type": "text",
                  "name": "question8_6_3",
                  "title": "سن ابتلا",
                  "isRequired": true,
                  "inputType": "number",
                  "min": 25,
                  "max": 120,
                  "minErrorText": "حداقل مقدار قابل قبول 25 است",
                  "maxErrorText": "حداکثر مقدار قابل قبول 120 است"
                },
                {
                  "type": "text",
                  "name": "question8_6_3_year",
                  "startWithNewLine": false,
                  "title": "سال تولد",
                  "isRequired": true,
                  "inputType": "number",
                  "min": 1300,
                  "max": 1402,
                  "minErrorText": "حداقل مقدار سال 1300 است",
                  "maxErrorText": "حداکثر مقدار سال 1402 است"
                }
              ],
              "panelCount": 1,
              "minPanelCount": 1,
              "maxPanelCount": 10,
              "confirmDelete": true,
              "panelAddText": "افزودن فرد مبتلا دیگر",
              "panelRemoveText": "حذف",
              "panelPrevText": "قبلی",
              "panelNextText": "بعدی"
            }
          ]
        },
        {
          "type": "panel",
          "name": "panel_question38",
          "elements": [
            {
              "type": "radiogroup",
              "name": "question38",
              "title": "آیا جهش در ژن های BRCA1 یا BRCA 2 در خانواده درجه یک (مادر، خواهر و یا دختر) دارید؟",
              "choices": [
                {
                  "value": "1",
                  "text": "تا کنون این تست را انجام نداده اند"
                },
                {
                  "value": "2",
                  "text": "این تست را انجام داده اند و نتیجه آن منفی بوده است"
                },
                {
                  "value": "3",
                  "text": "این تست را انجام داده اند و نتیجه آن مثبت (جهش در یکی از این ژن ها) بوده است"
                },
                {
                  "value": "4",
                  "text": "نمی دانم"
                }
              ]
            }
          ]
        }
      ]
    },
    {
      "name": "page4",
      "title": "علایم در خودآزمایی",
      "elements": [
        {
          "type": "panel",
          "name": "panel_9",
          "elements": [
            {
              "type": "radiogroup",
              "name": "question9",
              "title": "آیا در خودآزمایی پستان، احساس توده(غده یا برجستگی غیرمعمول) در پستان می‌کنید؟",
              "isRequired": true,
              "choices": [
                {
                  "value": "false",
                  "text": "خیر"
                },
                {
                  "value": "leftSide",
                  "text": "بلی در پستان چپ"
                },
                {
                  "value": "rightSide",
                  "text": "بلی در پستان راست"
                },
                {
                  "value": "bothSide",
                  "text": "بلی در هردو پستان"
                }
              ]
            },
            {
              "type": "checkbox",
              "name": "question9_1_1",
              "visibleIf": "{question9} anyof ['leftSide', 'bothSide']",
              "title": "محل توده پستان چپ",
              "isRequired": true,
              "choices": [
                {
                  "value": "1",
                  "text": "یک چهارم بالایی داخلی"
                },
                {
                  "value": "2",
                  "text": "یک چهارم بالایی خارجی"
                },
                {
                  "value": "3",
                  "text": "یک چهارم پایینی داخلی"
                },
                {
                  "value": "4",
                  "text": "یک چهارم پایینی خارجی"
                },
                {
                  "value": "5",
                  "text": "زیر نوک پستان"
                }
              ]
            },
            {
              "type": "checkbox",
              "name": "question9_2_1",
              "visibleIf": "{question9} anyof ['bothSide', 'rightSide']",
              "title": "محل توده پستان راست",
              "isRequired": true,
              "choices": [
                {
                  "value": "1",
                  "text": "یک چهارم بالایی داخلی"
                },
                {
                  "value": "2",
                  "text": "یک چهارم بالایی خارجی"
                },
                {
                  "value": "3",
                  "text": "یک چهارم پایینی داخلی"
                },
                {
                  "value": "4",
                  "text": "یک چهارم پایینی خارجی"
                },
                {
                  "value": "5",
                  "text": "زیر نوک پستان"
                }
              ]
            }
          ]
        },
        {
          "type": "panel",
          "name": "panel_10",
          "elements": [
            {
              "type": "radiogroup",
              "name": "question10",
              "title": "آیا در خودآزمایی، احساس توده(غده یا برجستگی غیرمعمول) در زیربغل می کنید؟",
              "isRequired": true,
              "choices": [
                {
                  "value": "false",
                  "text": "خیر"
                },
                {
                  "value": "leftSide",
                  "text": "بلی در سمت چپ"
                },
                {
                  "value": "rightSide",
                  "text": "بلی در سمت راست"
                },
                {
                  "value": "bothSide",
                  "text": "بلی در هردو طرف"
                }
              ]
            }
          ]
        },
        {
          "type": "panel",
          "name": "panel_11",
          "elements": [
            {
              "type": "radiogroup",
              "name": "question11",
              "title": "آیا در خودآزمایی، در ظاهر کلی پستان تغییراتی مشاهده می کنید؟",
              "isRequired": true,
              "choices": [
                {
                  "value": "false",
                  "text": "خیر"
                },
                {
                  "value": "leftSide",
                  "text": "بلی در پستان چپ"
                },
                {
                  "value": "rightSide",
                  "text": "بلی در پستان راست"
                },
                {
                  "value": "bothSide",
                  "text": "بلی در هردو پستان"
                }
              ]
            },
            {
              "type": "checkbox",
              "name": "question11_1",
              "visibleIf": "{question11} anyof ['leftSide', 'bothSide']",
              "title": "تغییرات ظاهری پستان چپ",
              "isRequired": true,
              "choices": [
                {
                  "value": "1",
                  "text": "تغییر در اندازه"
                },
                {
                  "value": "2",
                  "text": "تغییر در شکل"
                },
                {
                  "value": "3",
                  "text": "تغییر در قوام"
                }
              ]
            },
            {
              "type": "checkbox",
              "name": "question11_2",
              "visibleIf": "{question11} anyof ['rightSide', 'bothSide']",
              "title": "تغییرات ظاهری پستان راست",
              "isRequired": true,
              "choices": [
                {
                  "value": "1",
                  "text": "تغییر در اندازه"
                },
                {
                  "value": "2",
                  "text": "تغییر در شکل"
                },
                {
                  "value": "3",
                  "text": "تغییر در قوام"
                }
              ]
            }
          ]
        },
        {
          "type": "panel",
          "name": "panel_12",
          "elements": [
            {
              "type": "radiogroup",
              "name": "question12",
              "title": "آیا در خودآزمایی، در پوست پستان تغییراتی مشاهده می کنید؟",
              "isRequired": true,
              "choices": [
                {
                  "value": "false",
                  "text": "خیر"
                },
                {
                  "value": "leftSide",
                  "text": "بلی در پستان چپ"
                },
                {
                  "value": "rightSide",
                  "text": "بلی در پستان راست"
                },
                {
                  "value": "bothSide",
                  "text": "بلی در هردو پستان"
                }
              ]
            },
            {
              "type": "checkbox",
              "name": "question12_1_1",
              "visibleIf": "{question12} anyof ['leftSide', 'bothSide']",
              "title": "تغییرات پستان چپ را چگونه توصیف می کنید؟",
              "isRequired": true,
              "choices": [
                {
                  "value": "1",
                  "text": "افزایش ضخامت"
                },
                {
                  "value": "2",
                  "text": "پوست پرتقالی"
                },
                {
                  "value": "3",
                  "text": "سوزش، قرمزی یا گرمی"
                },
                {
                  "value": "4",
                  "text": "زخم"
                },
                {
                  "value": "5",
                  "text": "پوسته پوسته شدن"
                },
                {
                  "value": "6",
                  "text": "تورفتگی"
                },
                {
                  "value": "7",
                  "text": "برآمدگی"
                }
              ]
            },
            {
              "type": "checkbox",
              "name": "question12_2_1",
              "visibleIf": "{question12} anyof ['rightSide', 'bothSide']",
              "title": "تغییرات پستان راست را چگونه توصیف می کنید؟",
              "isRequired": true,
              "choices": [
                {
                  "value": "1",
                  "text": "افزایش ضخامت"
                },
                {
                  "value": "2",
                  "text": "پوست پرتقالی"
                },
                {
                  "value": "3",
                  "text": "سوزش، قرمزی یا گرمی"
                },
                {
                  "value": "4",
                  "text": "زخم"
                },
                {
                  "value": "5",
                  "text": "پوسته پوسته شدن"
                },
                {
                  "value": "6",
                  "text": "تورفتگی"
                },
                {
                  "value": "7",
                  "text": "برآمدگی"
                }
              ]
            }
          ]
        },
        {
          "type": "panel",
          "name": "panel_99",
          "elements": [
            {
              "type": "radiogroup",
              "name": "question99",
              "title": "آیا در خودآزمایی، در نوک پستان تغییراتی مشاهده می کنید؟",
              "isRequired": true,
              "choices": [
                {
                  "value": "false",
                  "text": "خیر"
                },
                {
                  "value": "leftSide",
                  "text": "بلی در پستان چپ"
                },
                {
                  "value": "rightSide",
                  "text": "بلی در پستان راست"
                },
                {
                  "value": "bothSide",
                  "text": "بلی در هردو پستان"
                }
              ]
            },
            {
              "type": "checkbox",
              "name": "question99_1_1",
              "visibleIf": "{question99} anyof ['rightSide', 'leftSide', 'bothSide']",
              "title": "این تغییرات را چگونه توصیف می کنید؟",
              "isRequired": true,
              "choices": [
                {
                  "value": "1",
                  "text": "قرمزی"
                },
                {
                  "value": "2",
                  "text": "زخم یا خراشیدگی"
                },
                {
                  "value": "3",
                  "text": "پوسته پوسته شدن و خارش"
                },
                {
                  "value": "4",
                  "text": "تورفتگی پیش رونده"
                },
                {
                  "value": "5",
                  "text": "تغییر جهت"
                }
              ]
            }
          ]
        },
        {
          "type": "panel",
          "name": "panel_13",
          "elements": [
            {
              "type": "radiogroup",
              "name": "question13",
              "title": "آیا در خودآزمایی، نوک پستان ترشحاتی دارد؟",
              "isRequired": true,
              "choices": [
                {
                  "value": "false",
                  "text": "خیر"
                },
                {
                  "value": "leftSide",
                  "text": "بلی در پستان چپ"
                },
                {
                  "value": "rightSide",
                  "text": "بلی در پستان راست"
                },
                {
                  "value": "bothSide",
                  "text": "بلی در هردو پستان"
                }
              ]
            },
            {
              "type": "checkbox",
              "name": "question13_1_1",
              "visibleIf": "{question13} anyof ['rightSide', 'leftSide', 'bothSide']",
              "title": "این ترشحات چگونه است؟",
              "isRequired": true,
              "choices": [
                {
                  "value": "1",
                  "text": "ترشح از یک پستان، نه هر دو پستان"
                },
                {
                  "value": "2",
                  "text": "ترشح خودبخودی و ادامه دار"
                },
                {
                  "value": "3",
                  "text": "ترشح در هنگامی که آن را لمس می کنید"
                },
                {
                  "value": "4",
                  "text": "ترشح خونی یا خونابه ای"
                }
              ]
            }
          ]
        }
      ]
    }
  ],
  "showQuestionNumbers": "off"
}