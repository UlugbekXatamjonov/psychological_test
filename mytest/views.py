from django.shortcuts import render, get_object_or_404

from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework import viewsets
from rest_framework.response import Response

from .models import Category, Info, Form, Form_number, Test, Test_answer, Test_result
from .models import Form_number as NumberModel
from .serializers import CategorySerializer, InfoSerializer, FormSerializer, Form_numberSerializer, TestSerializer, \
    Test_answerSerializer, Test_resultSerializer

# Create your views here.

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    permission_classes = [AllowAny] 
    
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
                    return Response({"name":"Bunday nomdagi kategoriya mavjud! Iltimos boshqa nom yozing"})                
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
                    )
            else:
                new_category = Category.objects.create(
                    name = category_data['name'],
                    body = category_data['body'],
                    category_form = category_data['category_form'],
                    ball35 = category_data['ball35'],
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
        # category = Category.objects.get(id=data['category'])
        
        # category =  False        
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
            )
            new_info.save()
            serializer = InfoSerializer(new_info)
            return Response(serializer.data)
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
            else:
                contact.full_name = data['full_name'] if 'full_name' in data else contact.full_name
                contact.age = data['age'] if 'age' in data else contact.age
                contact.gender = data['gender'] if 'gender' in data else contact.gender
            contact.save()
            serializer = InfoSerializer(contact)
            return Response(serializer.data)
        except Exception as e:
            return Response({'errors':"Ma'lumotlarni saqlashda xatolik sodir bo'ladi!!!"})

    def total_score(self, request, *args, **kwargs):
        # def tests_answer(selected_answers):
        """ Kelayotgan resuest dan belgilangan category va test hamda uning variantlarini yuklab olamiz """
        answer_category = request.get('category') # belgilangan category idsi
        answer_tests = request.get['tests'] # belgilangan test va javob idlari
        
        answer_tests_id = [] # belgilangan test idlari
        for test in answer_tests:
            answer_tests_id.append(test['test_id'])
            
        answer_answer_id = [] # belgilangan javoblar idlari
        for awr in answer_tests:
            answer_answer_id.append(awr['answer_id'])
            
        """ requstdan kelgan test va kategoriya idlari asosida o'zimizda bor test va category larni yig'ib olamiz """
        category = Category.objects.filter(id=answer_category) # belgilangan category obyekti
        
        total_tests = [] # belgilangan test obyekti(ro'yhat)
        for testid in answer_tests_id:
            total_tests.append(Test.objects.filter(id=testid))
        
        """ testlarni formulasi bo'yicha ajratib olamiz; E1 va E2 """    
        test_e1 = [] # belgilangan E1 test obyekti(ro'yhat)
        for testid in answer_tests_id:
            test_e1.append(Test.objects.filter(id=testid, form=1))
            
        test_e2 = [] # belgilangan E2 test obyekti(ro'yhat)
        for testid in answer_tests_id:
            test_e2.append(Test.objects.filter(id=testid, form=2)) 
        
        """ Javoblarni ham ajratib olamiz """
        answer = [] # belgilangan answer obyekti(ro'yhat)
        for answerid in answer_answer_id:
            answer.append(Test_answer.objects.filter(id=answerid))
        
        """ E1 turidagi teslarni idsi javoblardagi 'test_id' bilan birxil bo'la; yani javob E1 turidagi
            testga tegishli bo'lsa o'sha javobni  'ball'lini 'e1' degan o'zgaruvchiga yig'amiz.
            Va natijada hamma E1 turidagi testlarning javoblari ostidagi ballar yig'indisini topamiz. 
            Huddi shu ish E2 turidagi testlar ushun ham takrorlangan. """
        
        """ E1 turidagi tstlar uchun """
        e1 = 0
        for test in test_e1:
            for asw in answer:
                if asw.test_id == test.id:
                    e1 += answer.ball
        """ E2 turidagi tstlar uchun """         
        e2 = 0
        for test in test_e2:
            for asw in answer:
                if asw.test_id == test.id:
                    e2 += answer.ball
                
        """  ---------------------   Ballni hisoblash ---------------------- """
        total_ball = 0 # ummumiy ball
        if category.ball35 > 0 and category == answer_category:
            """ E1-E2+35 """
            total_ball = e1 - e2 + category.ball35
        elif category.ball35 == 0 and category == answer_category:
            total_ball = e1 + e2
        else:
            print("Ballni hisoblashda xatolik sodir bo'ldi!!!")

        return(total_ball)



class FormViewSet(viewsets.ModelViewSet):
    queryset = Form.objects.all()
    serializer_class = FormSerializer
    lookup_field = 'slug'
    permission_classes = [AllowAny]
    
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


class Form_numberViewSet(viewsets.ModelViewSet):
    queryset = Form_number.objects.all()
    serializer_class = Form_numberSerializer    
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        form_number_data = request.data

        category =  False        
        if 'category' in form_number_data:
            try:
                category = Category.objects.get(pk=form_number_data['category'])
            except Exception as e:
                return Response({"category":"Bunday Categoriya mavjud emas!!!"})
            
        form =  False        
        if 'form' in form_number_data:
            try:
                form = Form.objects.get(pk=form_number_data['form'])
            except Exception as e:
                return Response({"form":"Bunday test mavjud emas!!!"})
        
          
        try:
            new_form_number = Form_number.objects.create(
                category = category,
                form = form,
                number = form_number_data['number'],
                )

            new_form_number.save()
            serializer = Form_numberSerializer(new_form_number)
            return Response(serializer.data)
        except Exception as e:
    	    return Response({'errors':"Ma'lumot to'liq emas!!!"})

    def destroy(self, request, *args, **kvargs):
        form_number = self.get_object()
        form_number.status = 'delete'
        form_number.delete()
        return Response({"message":"Ma'lumot muvaffaqiyatli o'chirildi."})
    
    def update(self, request, *args, **kwargs):
        form_number = self.get_object()
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
            form_number.name = data['name'] if 'name' in data else form_number.name
            form_number.category = category
            form_number.form = form
            
            form_number.save()
            serializer = Form_numberSerializer(form_number)
            return Response(serializer.data)
        except Exception as e:
            return Response({'errors':"Ma'lumotlarni saqlashda xatolik sodir bo'ladi!!!"})


class TestViewSet(viewsets.ModelViewSet):   
    queryset = Test.objects.all()
    serializer_class = TestSerializer
    lookup_field = 'slug'
    permission_classes = [AllowAny]
        
    def create(self, request, *args, **kwargs):
        test_data = request.data

        category =  False        
        if 'category' in test_data:
            try:
                category = Category.objects.get(pk=test_data['category'])
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
                test_data.form = form
                test_data.category = category
                test_data.body = data['body'] if 'body' in data else test_data.body
            else:
                test_data.form = form if form else test_data.form
                test_data.body = data['body'] if 'body' in data else test_data.body
            test_data.save()
            serializer = TestSerializer(test_data)
            return Response(serializer.data)
        except Exception as e:
            return Response({'errors':"Ma'lumotlarni saqlashda xatolik sodir bo'ladi!!!"})


class TestAnswerViewSet(viewsets.ModelViewSet):
    queryset = Test_answer.objects.all()
    serializer_class = Test_answerSerializer
    permission_classes  =[AllowAny]

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
            else:
                test_answear_data.answer_text = data['answer_text'] if 'answer_text' in data else test_answear_data.answer_text
                test_answear_data.ball = data['ball'] if 'ball' in data else test_answear_data.ball
            test_answear_data.save()
            serializer = Test_answerSerializer(test_answear_data)
            return Response(serializer.data)
        except Exception as e:
            return Response({'errors':"Ma'lumotlarni saqlashda xatolik sodir bo'ladi!!!"})


class TestResultViewSet(viewsets.ModelViewSet):
    queryset = Test_result.objects.all()
    serializer_class = Test_resultSerializer
    permission_classes  =[AllowAny]
        
    def create(self, request, *args, **kwargs):
        test_result_data = request.data

        info_id =  False        
        if 'info_id' in test_result_data:
            try:
                info_id = Info.objects.get(pk=test_result_data['info_id'])
            except Exception as e:
                return Response({"info_id":"Bunday info mavjud emas!!!"})
            
        test_id =  False        
        if 'test_id' in test_result_data:
            try:
                test_id = Test.objects.get(pk=test_result_data['test_id'])
            except Exception as e:
                return Response({"test_id":"Bunday test mavjud emas!!!"})
        
        answer_id =  False        
        if 'answer_id' in test_result_data:
            try:
                answer_id = Test_answer.objects.get(pk=test_result_data['answer_id'])
            except Exception as e:
                return Response({"answer_id":"Bunday javob mavjud emas!!!"})
            
          
        try:
            new_test_result = Test_result.objects.create(
                info_id = info_id,
                test_id = test_id,
                answer_id = answer_id,
                diagnosis = test_result_data['diagnosis'],
                )

            new_test_result.save()
            serializer = Test_resultSerializer(new_test_result)
            return Response(serializer.data)
        except Exception as e:
    	    return Response({'errors':"Ma'lumot to'liq emas!!!"})

            
    def destroy(self, request, *args, **kvargs):
        test_result = self.get_object()
        test_result.status = 'delete'
        test_result.delete()   
        return Response({"message":"Ma'lumot muvaffaqiyatli o'chirildi."})
    
   
    def update(self, request, *args, **kwargs):
        """Test result taxrirlanmasli sababli update() to'liq yozilmadi yozilmadi"""
        test_result_data = self.get_object()
        data = request.data
        
        try:
        	try:
           		info_id = Info.objects.filter(pk=data['info_id']).first()
        	except:
            	    info_id = None
        except Exception as e:
            return Response({"error":"Bunday  Info mavjud emas!!!"})
    
        try:
        	try:
           		test_id = Test.objects.filter(pk=data['test_id']).first()
        	except:
            	    test_id = None
        except Exception as e:
            return Response({"error":"Bunday  Test mavjud emas!!!"})
        
        try:
        	try:
           		answer_id = Test_answer.objects.filter(pk=data['answer_id']).first()
        	except:
            	    answer_id = None
        except Exception as e:
            return Response({"error":"Bunday  Ansver mavjud emas!!!"})
        
        try: 
            test_result_data.info_id = info_id
            test_result_data.test_id = test_id
            test_result_data.answer_id = answer_id
            test_result_data.diagnosis = data['diagnosis'] if 'diagnosis' in data else test_result_data.diagnosis
            test_result_data.save()
            serializer = Test_resultSerializer(test_result_data)
            return Response(serializer.data)
        except Exception as e:
            return Response({'errors':"Ma'lumotlarni saqlashda xatolik sodir bo'ladi!!!"})




