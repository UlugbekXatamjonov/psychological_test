from django.shortcuts import render, get_object_or_404

from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework import viewsets
from rest_framework.response import Response

from .models import Category, Info, Form, Test, Test_answer
from .serializers import CategorySerializer, InfoSerializer, FormSerializer, TestSerializer, \
    Test_answerSerializer

import json
from pprint import pprint

# Create your views here.

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    permission_classes = [IsAuthenticated] 
    
    def create(self, request, *args, **kwargs):
        category_data = request.data

        # start <--- Category Foreginkeyi uchun ---> 
        parent =  False
        if 'parent' in category_data:
            try:
                parent = Category.objects.get(pk=category_data['parent'])
            except Exception as e:
                return Response({"parent":"Bunday Katta kategoriya mavjud emas!!!"})
        # end  <--- Category Foreginkeyi uchun --->

        # start  <--- Bir Categoriya ikki marta takrorlanmasligi un  --->
        categories = Category.objects.filter(status='active')   
        for category in categories:
                if category.name == category_data['name']:
                    return Response({"error":"Bunday nomdagi kategoriya mavjud! Iltimos boshqa nom yozing"})                
        # and  <--- Bir Categoriya ikki marta takrorlanmasligi un  --->
        
        try:
            # start  <--- parent maydoni ihtiyoriy bo'lgani un agar u kiritilsa if kiritilmasa esle --->
            if parent:
                new_category = Category.objects.create(
                    parent =  parent,
                    name = category_data['name'],
                    body = category_data['body'],
                    category_form = category_data['category_form'],
                    ball35 = category_data['ball35'],
                    tur = category_data['tur'],
                    )
            else:
                new_category = Category.objects.create(
                    name = category_data['name'],
                    body = category_data['body'],
                    category_form = category_data['category_form'],
                    ball35 = category_data['ball35'],
                    tur = category_data['tur'],
                    )
             # and  <--- parent maydoni ihtiyoriy bo'lgani un agar u kiritilsa if kiritilmasa esle --->
             
            new_category.save()
            serializer = CategorySerializer(new_category)
            return Response(serializer.data)
        except Exception as e:
    	    return Response({'errors':"Ma'lumot to'liq emas!!!"})

    def destroy(self, request, *args, **kvargs):
        category = self.get_object()
        category.status = 'delete'
        category.delete()
        return Response({"message":"Ma'lumot muvaffaqiyatli o'chirildi."})

    def update(self, request, *args, **kwargs):
        contact = self.get_object()
        data = request.data

        # <--- Foreginkey uchun --->
        try:
        	try:
           		parent = Category.objects.filter(pk=data['parent']).first()
        	except:
            		parent = None
        except Exception as e:
            return Response({"error":"Bunday  Kata kategoriya mavjud emas!!!"})
        # <--- Foreginkey uchun --->

        try:
            contact.name = data['name'] if 'name' in data else contact.name
            contact.parent = parent if parent else contact.parent
            contact.body = data['body'] if 'body' in data else contact.body
            contact.category_form = data['category_form'] if 'category_form' in data else contact.category_form
            contact.ball35 = data['ball35'] if 'ball35' in data else contact.ball35
            contact.status = data['status'] if 'status' in data else contact.status
            contact.tur = data['tur'] if 'tur' in data else contact.tur

            contact.save()
            serializer = CategorySerializer(contact)
            return Response(serializer.data)
        except Exception as e:
            return Response({'errors':"Ma'lumotlarni saqlashda xatolik sodir bo'ladi!!!"})  


class InfoViewSet(viewsets.ModelViewSet):
    queryset = Info.objects.all()
    serializer_class = InfoSerializer
    lookup_field = 'slug'
    permission_classes = [AllowAny]   

    def create(self, request, *args, **kwargs):
        data = request.data
        api0 = json.loads(request.data['test_api'])
        api = api0[0]
        # print("***************************")
        # pprint(data)
        # print("***************************")
        # pprint(api)
        # print("***************************")
        
        
        """ 
        ##########################################################################################################
        ##########################################################################################################
                        ✅ Belgilangan javoblar asosida ummumiy balni hisoblash va tashxis qo'yish ✅
        ##########################################################################################################
        ##########################################################################################################
        """
        
        """ Kelayotgan request dan belgilangan category, test va tesning  javoblarini o'zgaruvchilarga yuklab olamiz """
        answer_category = api.get('category') # belgilangan category idsi
        answer_tests = api.get('tests') # belgilangan test va javob idlari
        
        answer_tests_id = [] # belgilangan test idlari
        for test in answer_tests:   
            answer_tests_id.append(test['test_id'])
            
        answer_answer_id = [] # belgilangan javoblar idlari
        for awr in answer_tests:
            answer_answer_id.append(awr['answer_id'])
            

        """ Requstdan kelgan test va kategoriya id lari asosida o'zimizda bor test va category larni yig'ib olamiz.
            Testlar bir yo'la 3 ta list qilib olingan; ummumiy(total_tests), E1 turidagi testlar(e1_tests), E2 turidagi testlar(e2_tests) 
        """
        category = Category.objects.filter(id=answer_category).values() # belgilangan category obyekti / bazadagi

        total_tests = [] # belgilangan test obyektlari(ro'yhati) / bazadagi
        e1_tests = [] # belgilangan E1 turidagi test obyektlari / bazadagi
        e2_tests = [] # belgilangan E2 turidagi test obyektlari / bazadagi
        
                    
        for testid in answer_tests_id:
            test = Test.objects.filter(id=testid).values()
            test_e1 = Test.objects.filter(form_id=1, id=testid).values()
            test_e2 = Test.objects.filter(form_id=2, id=testid).values()
        
            if bool(test):
                total_tests.append(test)
        
            if bool(test_e1):
                e1_tests.append(test_e1)
        
            if bool(test_e2):
                e2_tests.append(test_e2)
            
            
        """ Javoblarni ham ajratib olamiz """
        total_answers = [] # belgilangan answer obyektlari ro'yhati
        for answerid in answer_answer_id:
            total_answers.append(Test_answer.objects.filter(id=answerid).values())
        
    
        """ E1 turidagi teslarni idsi javoblardagi 'test_id' bilan birxil bo'la; yani javob E1 turidagi
            testga tegishli bo'lsa o'sha javobni  'ball' lini 'e1' degan o'zgaruvchiga yig'amiz.
            Va natijada hamma E1 turidagi testlarning javoblari ostidagi ballar yig'indisini topamiz. 
            Huddi shu ish E2 turidagi testlar ushun ham takrorlangan. 
        """
        
        
        
        # print("---------------------")    
        # pprint(total_answers[0]['ball'])
        
        # print("---------------------")

        """ Barcha testlar uchun """
        t_ball = 0 # hamma javoblardagi ballar yi'gindisi   
        for answer in total_answers:
            t_ball += answer[0]['ball']
        # print(f"Total BALLS ----> {t_ball}")
        
        
        """ E1 turidagi testlar uchun """
        e1_ball = 0 # E1 turidagi testlarning  javobidagi ballar yi'gindisi
        for test in e1_tests:    
            for answer in total_answers:
                if answer[0]['test_id_id'] == test[0]['id']:
                    e1_ball += answer[0]['ball']
        # print(f"Total E1 BALL ----> {e1_ball}")
        
                  
        """ E2 turidagi tstlar uchun """         
        e2_ball = 0  # E2 turidagi testlarning  javobidagi ballar yi'gindisi
        for test in e2_tests:    
            for answer in total_answers:
                if answer[0]['test_id_id'] == test[0]['id']: 
                    e2_ball += answer[0]['ball']
        # print(f"Total E2 BALL ----> {e2_ball}")
                
                
            
        """ ---------------------   Ballni hisoblash ---------------------- """
    
        total_ball = 0 # testning ummumiy balli
        tashxis = " Tashxis hali qo'yilmagan "
        tafsiya = False
        xavotir = False
        depressiya = False
        boshqa = False
        
        if category[0]['tur'] == 'xavotir':
            xavotir = True
        if category[0]['tur'] == 'depressiya':
            depressiya = True
        if category[0]['tur'] == 'boshqa':
            boshqa = True
        
        
        ishora_1 = 0
        ishora_2 = 0
        
        
        if category[0]['category_form']:# ✅✅✅ Sinovdan o'tdi
            ishora_1 = 1
            if category[0]['ball35']: # ✅✅✅ Sinovdan o'tdi
                total_ball += e1_ball - e2_ball + category[0]['ball35']# E1 - E2 + 35 ball
                # print(f"E1 {e1_ball} - E2 {e2_ball} + Ball35 + {category[0]['ball35']}")
                ishora_2 = 1
                """ Tashxis """
                if total_ball <= 30:
                    tashxis = "Yengil daraja"
                elif total_ball <= 45:
                    tashxis = "O'rta daraja"
                    tafsiya = True
                elif total_ball >= 46:
                    tashxis = "Kuchli daraja"
                    tafsiya = True
                else:
                    tashxis = "Tashxis qo'yishda xatolik !!!"
                # print(tashxis)
                
            else: # ✅✅✅ Sinovdan o'tdi
                total_ball += e1_ball + e2_ball # E1 + E2
                # print(f"E1 {e1_ball} + E2 {e2_ball}")
                
                """ Tashxis """
                if total_ball <= 40:
                    tashxis = "Yo'q "
                elif total_ball <= 48:
                    tashxis = "Yengil daraja "
                elif total_ball <= 55:
                    tashxis = "O'rta daraja "
                    tafsiya = True
                elif total_ball <= 82:
                    tashxis = "Og'ir daraja"
                    tafsiya = True
                else:
                    tashxis = "Tashxis qo'yishda xatolik !!!"
                # print(tashxis)
                    
        elif xavotir:
            total_ball += t_ball # Javobdagi barcha ballar yig'indisi
            # print(f"t_ball = {t_ball}")
            
            """ Tashxis """
            if total_ball <= 7:
                tashxis = "Norma"
            elif total_ball <= 10:
                tashxis = "Subklinik xavotir"
                tafsiya = True
            elif total_ball >= 11:
                tashxis = "Kuchlik xavotir"
                tafsiya = True
            else:
                tashxis = "Tashxis qo'yishda xatolik !!!"
            # print(tashxis)
            
        elif depressiya:
            total_ball += t_ball # Javobdagi barcha ballar yig'indisi
            # print(f"t_ball = {t_ball}")
            
            """ Tashxis """
            if total_ball <= 7:
                tashxis = "Norma"
            elif total_ball <= 10:
                tashxis = "Subklinik Dipressia"
                tafsiya = True
            elif total_ball >= 11:
                tashxis = "Kuchlik Dipressia"
                tafsiya = True
            else:
                tashxis = "Tashxis qo'yishda xatolik !!!"
                
        elif boshqa:
            total_ball += t_ball # Javobdagi barcha ballar yig'indisi
            # print(f"t_ball = {t_ball}")
            
            """ Tashxis """
            if total_ball <= 7:
                tashxis = "Norma"
            elif total_ball <= 10:
                tashxis = "Subklinik"
                tafsiya = True
            elif total_ball >= 11:
                tashxis = "Kuchlik"
                tafsiya = True
            else:
                tashxis = "Tashxis qo'yishda xatolik !!!"
            # print(tashxis)
            
        # else:
        #     total_ball += t_ball # Javobdagi barcha ballar yig'indisi
        #     # print(f"t_ball = {t_ball}")
            
        #     """ Tashxis """
        #     if total_ball <= 7:
        #         tashxis = "Norma"
        #     elif total_ball <= 10:
        #         tashxis = "Subklinik xavotir / Dipressia"
        #         tafsiya = True
        #     elif total_ball >= 11:
        #         tashxis = "Kuchlik xavotir / Dipressia"
        #         tafsiya = True
        #     else:
        #         tashxis = "Tashxis qo'yishda xatolik !!!"
            # print(tashxis)
            
            
            

        # print(f"Testning ummumiy balli --> {total_ball}")
        
        """ 
        ##########################################################################################################
        ##########################################################################################################
                        ✅ Belgilangan javoblar asosida ummumiy balni hisoblash va tashxis qo'yish ✅
        ##########################################################################################################
        ##########################################################################################################
        """
        
        
        
        """ 👇👇👇 Yangi obyekt yaratish 👇👇👇 """
        
        testes_api = {  # API Frontdan keladi, uni qayta ishlaymiz, keyin u kelgan maydonga shuni qo'yib ketamiz
            "api": "Bu yerda API bo'ladi :)"
        } 
    
        if 'category' in data:
            try:
                category = Category.objects.get(pk=data['category'])
            except Exception as e:
                return Response({"category":"Bunday Kategoriya mavjud emas!!!"})
        
        try:
            new_info = Info.objects.create(
                category = category,
                full_name = data['full_name'],
                gender = data['gender'],
                age = data['age'],
                test_ball = total_ball, # testning umumiy bali
                test_result = tashxis, # testning tashxisi
                test_api = testes_api # frontdan kelgan API o'rniga shunchaki 
            )
            new_info.save()
            serializer = InfoSerializer(new_info)
            # return Response(serializer.data) # javob ketishi kk shu yerda
            
            if ishora_1:
                if ishora_2: # E1 - E2 + 35 ball
                    if tafsiya:
                        return Response({'message':f"Hurmatli {data['full_name']} ! Sizning testdan toplagan ballingiz: {total_ball} ball",
                                        'tashxis':f"Xulosa: {tashxis}",
                                        "tafsiya":"Mutahasis tafsiyasini oling.",
                                        "doctor":"Shifokor, Tibbiy psixolog, psixoterapeft - Dedaxanov Dilshod Toxirovich",
                                        "tel":"Tel: +998902750030"
                                        })
                    else:
                        return Response({'message':f"Hurmatli {data['full_name']} ! Sizning testdan toplagan ballingiz: {total_ball} ball",
                                        'tashxis':f"Xulosa: {tashxis}"
                                        })
                else: # E1 + E2
                    if tafsiya:
                        return Response({'message':f"Hurmatli {data['full_name']} ! Sizning testdan toplagan ballingiz: {total_ball} ball",
                                        'tashxis':f"Xulosa: {tashxis}",
                                        "tafsiya":"Mutahasis tafsiyasini oling.",
                                        "doctor":"Shifokor, Tibbiy psixolog, psixoterapeft - Dedaxanov Dilshod Toxirovich",
                                        "tel":"Tel: +998902750030"
                                        })
                    else:
                        return Response({'message':f"Hurmatli {data['full_name']} ! Sizning testdan toplagan ballingiz: {total_ball} ball",
                                        'tashxis':f"Xulosa: {tashxis}"
                                        })   
            else: # Javobdagi barcha ballar yig'indisi   
                if tafsiya:
                    return Response({'message':f"Hurmatli {data['full_name']} ! Sizning testdan toplagan ballingiz: {total_ball} ball",
                                    'tashxis':f"Xulosa: {tashxis}",
                                    "tafsiya":"Mutahasis tafsiyasini oling.",
                                    "doctor":"Shifokor, Tibbiy psixolog, psixoterapeft - Dedaxanov Dilshod Toxirovich",
                                    "tel":"Tel: +998902750030"
                                    })
                else:
                    return Response({'message':f"Hurmatli {data['full_name']} ! Sizning testdan toplagan ballingiz: {total_ball} ball",
                                    'tashxis':f"Xulosa: {tashxis}"
                                    })
                    
        except Exception as e:
            return Response({'errors':"Ma'lumot to'liq emas!!!"})

    def destroy(self, request, *args, **kvargs):
        info = self.get_object()
        info.status = 'delete'
        info.delete()
        return Response({"message":"Ma'lumot muvaffaqiyatli o'chirildi."})

    def update(self, request, *args, **kwargs):
        contact = self.get_object()
        data = request.data

        # <--- Foreginkey uchun ---> #
        try:
        	try:
           		category = Category.objects.filter(pk=data['category']).first()
        	except:
            	    category = None
        except Exception as e:
            return Response({"error":"Bunday kategoriya mavjud emas!!!"})
        # <--- Foreginkey uchun --->
        
        try:
            if category:
                contact.category = category # <--- Foreginkey uchun --->
                contact.full_name = data['full_name'] if 'full_name' in data else contact.full_name
                contact.age = data['age'] if 'age' in data else contact.age
                contact.gender = data['gender'] if 'gender' in data else contact.gender
                contact.test_ball = total_ball # testning balli
                contact.test_result = tashxis # testning tashxisi
                contact.test_api = data['test_api'] if 'test_api' in data else contact.test_api
                contact.test_api = data['test_api'] if 'test_api' in data else contact.test_api
            else:
                contact.full_name = data['full_name'] if 'full_name' in data else contact.full_name
                contact.age = data['age'] if 'age' in data else contact.age
                contact.gender = data['gender'] if 'gender' in data else contact.gender
                contact.test_ball = total_ball # testning balli
                contact.test_result = tashxis # testning tashxisi
                contact.test_api = data['test_api'] if 'test_api' in data else contact.test_api
                contact.test_api = data['test_api'] if 'test_api' in data else contact.test_api
            contact.save()
            serializer = InfoSerializer(contact)
            return Response(serializer.data)
        except Exception as e:
            return Response({'errors':"Ma'lumotlarni saqlashda xatolik sodir bo'ladi!!!"})

    

class FormViewSet(viewsets.ModelViewSet):
    queryset = Form.objects.all()
    serializer_class = FormSerializer
    lookup_field = 'slug'
    permission_classes = [IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        data = request.data
        try:
            new_form = Form.objects.create(
                name = data['name'],
            )
            new_form.save()
            serializer = FormSerializer(new_form)
            return Response(serializer.data)
        except Exception as e:
            return Response({'errors':"Ma'lumot to'liq emas!!!"})
    
    def destroy(self, request, *args, **kvargs):
        form = self.get_object()
        form.status = 'delete'
        form.delete()
        return Response({"message":"Ma'lumot muvaffaqiyatli o'chirildi."})
    
    def update(self, request, *args, **kwargs):
        form = self.get_object()
        data = request.data
        try:
            form.name = data['name'] if 'name' in data else form.name
            form.save()
            serializer = FormSerializer(form)
            return Response(serializer.data)
        except Exception as e:
            return Response({'errors':"Ma'lumotlarni saqlashda xatolik sodir bo'ladi!!!"})



class TestViewSet(viewsets.ModelViewSet):   
    queryset = Test.objects.all()
    serializer_class = TestSerializer
    lookup_field = 'slug'
    permission_classes = [IsAuthenticated]
        
    def create(self, request, *args, **kwargs):
        test_data = request.data

        category =  False        
        if 'category' in test_data:
            try:
                category = Category.objects.get(pk=str(test_data['category']))
            except Exception as e:
                return Response({"category":"Bunday Kategoriya mavjud emas!!!"})
            
        form =  False        
        if 'form' in test_data:
            try:
                form = Form.objects.get(pk=test_data['form'])
            except Exception as e:
                return Response({"form":"Bunday Form mavjud emas!!!"})
            
        try:
            if form:    
                new_form_number = Test.objects.create(
                    category = category,
                    form = form,
                    body = test_data['body'],
                    )
            else:
                new_form_number = Test.objects.create(
                    category = category,
                    body = test_data['body'],
                    )

            new_form_number.save()
            serializer = TestSerializer(new_form_number)
            return Response(serializer.data)
        except Exception as e:
    	    return Response({'errors':"Ma'lumot to'liq emas!!!"})

        
    def destroy(self, request, *args, **kvargs):
        test = self.get_object()
        test.status = 'delete'
        test.delete()   
        return Response({"message":"Ma'lumot muvaffaqiyatli o'chirildi."})
    
   
    def update(self, request, *args, **kwargs):
        test_data = self.get_object()
        data = request.data

        # <--- Category uchun --->
        try:
        	try:
           		category = Category.objects.filter(pk=data['category']).first()
        	except:
            		category = None
        except Exception as e:
            return Response({"error":"Bunday  Kata kategoriya mavjud emas!!!"})
        
        # <--- Form_number uchun   --->
        try:
        	try:
           		form = Form.objects.filter(pk=data['form']).first()
        	except:
            		form = None
        except Exception as e:
            return Response({"error":"Bunday  Forma mavjud emas!!!"})
        # <--- Foreginkey uchun --->
        
        try:
            if category:
                test_data.form = form if form else test_data.form
                test_data.category = category
                test_data.body = data['body'] if 'body' in data else test_data.body
                test_data.status = data['status'] if 'status' in data else test_data.status
            else:
                test_data.form = form if form else test_data.form
                test_data.body = data['body'] if 'body' in data else test_data.body
                test_data.status = data['status'] if 'status' in data else test_data.status
            test_data.save()
            serializer = TestSerializer(test_data)
            return Response(serializer.data)
        except Exception as e:
            return Response({'errors':"Ma'lumotlarni saqlashda xatolik sodir bo'ladi!!!"})


class TestAnswerViewSet(viewsets.ModelViewSet):
    queryset = Test_answer.objects.all()
    serializer_class = Test_answerSerializer
    permission_classes  =[IsAuthenticated]

    def create(self, request, *args, **kwargs):
        test_answear_data = request.data

        test_id =  False        
        if 'test_id' in test_answear_data:
            try:
                test_id = Test.objects.get(pk=test_answear_data['test_id'])
            except Exception as e:
                return Response({"test_id":"Bunday Test mavjud emas!!!"})
            
        try:
            new_test_answear = Test_answer.objects.create(
                test_id = test_id,
                answer_text = test_answear_data['answer_text'],
                ball = test_answear_data['ball'],
                )
            new_test_answear.save()
            serializer = Test_answerSerializer(new_test_answear)
            return Response(serializer.data)
        except Exception as e:
    	    return Response({'errors':"Ma'lumot to'liq emas!!!"})

            
    def destroy(self, request, *args, **kvargs):
        test_answear = self.get_object()
        test_answear.status = 'delete'
        test_answear.delete()   
        return Response({"message":"Ma'lumot muvaffaqiyatli o'chirildi."})
    
   
    def update(self, request, *args, **kwargs):
        test_answear_data = self.get_object()
        data = request.data
        
        # <--- Test uchun   --->
        try:
        	try:
           		test_id = Test.objects.filter(pk=data['test_id']).first()
        	except:
            	    test_id = None
        except Exception as e:
            return Response({"error":"Bunday  Test mavjud emas!!!"})
        # <--- Test uchun --->
        
        try:
            if test_id:    
                test_answear_data.test_id = test_id
                test_answear_data.answer_text = data['answer_text'] if 'answer_text' in data else test_answear_data.answer_text
                test_answear_data.ball = data['ball'] if 'ball' in data else test_answear_data.ball
                test_answear_data.status = data['status'] if 'status' in data else test_answear_data.status
            else:
                test_answear_data.answer_text = data['answer_text'] if 'answer_text' in data else test_answear_data.answer_text
                test_answear_data.ball = data['ball'] if 'ball' in data else test_answear_data.ball
                test_answear_data.status = data['status'] if 'status' in data else test_answear_data.status
            test_answear_data.save()
            serializer = Test_answerSerializer(test_answear_data)
            return Response(serializer.data)
        except Exception as e:
            return Response({'errors':"Ma'lumotlarni saqlashda xatolik sodir bo'ladi!!!"})






