# coding: utf-8
from vkbottle import Bot, Message
import vk_api
from vkbottle.keyboard import Keyboard, Text 
import json
import threading
import random
import time
import config
import vkcoin
import vk_api
from SimpleQIWI import *

otsyv = 'vk.com/topic-197173255_41649634' # Ссылку на отзывы

qiwi = {}

op = {}
po = {}


course = config.course
course_sale = config.course_sale
logic = { }
spisok = {}
comment = {}



bot = Bot( 'e87ce7d5121ce273cb4cdc11abca24e09af9c4c91a24cbc22956c7c67c56029024e99cbd942a2c87e8525', mobile = True )
vk = vk_api.VkApi( token =  'e87ce7d5121ce273cb4cdc11abca24e09af9c4c91a24cbc22956c7c67c56029024e99cbd942a2c87e8525' ).get_api()
merchant = vkcoin.VKCoin( user_id = config.user_id, key = config.key )
api = QApi( token = config.token_qiwi, phone = config.phone )

main = Keyboard(  )
main.add_row( )
main.add_button( Text( label = '📥Купить' ), color = 'positive' )
main.add_button( Text( label = '📤Продать' ), color = 'negative' )

main.add_row( )
main.add_button( Text( label = '📊 Информация' ), color = 'primary' )



@bot.on.message( text = '<text>', lower = True )
async def yes( ans: Message, text ):
	if text in [ 'Начать', 'Купить', 'Продать', 'Курс', 'начать', 'Меню', 'меню', 'курс', 'купить', 'продать', '📊 Информация', '📥Купить', '📤Продать' ]:
		if text in [ 'Начать', 'начать', 'меню', 'Меню' ] :
			tex = f"👑 Добро пожаловать! Это бот автоматической продажи и покупки коинов. \n\n❗ Перед покупкой/продажей обязательно прочитайте правила проведения сделок! vk.com/@gragonshop1-instrukciya-pered-pokupkoiprodazh..\n\n 📤 Продаем - { course_sale / 100 } руб за 1 000 000 коинов. \n 📥 Покупаем - { course / 100 } руб за 1 000 000 коинов. \n\n ❗ Автоматическая сделка только через киви. 🔔 Другие способы оплаты ( вручную через [garanterik|администратора] ): Sberbank/Qiwi card/Yandex Money/Tinkoff"
			await ans( message = tex , keyboard = main )
		
		elif text in [ '📊 Информация', 'курс' ]:
			await ans( f'Обязательно прочитайте правила проведения сделок! vk.com/@gragonshop1-instrukciya-pered-pokupkoiprodazh..\n\n 📤 Продаем - { course_sale / 100 } руб за 1 000 000 коинов. \n 📥 Покупаем - { course / 100 } руб за 1 000 000 коинов. \n\n 🔔 Другие способы оплаты ( вручную через [garanterik|администратора] ): Sberbank/Qiwi card/Yandex Money/Tinkoff' )
			
		elif text in [ '📥Купить', 'купить' ]:
			await ans( f'💥 Вы можете купить: { int( merchant.get_balance( 565905555 )[ str( 565905555 ) ] ) / 1000 } VkCoin.\n\n📤 Курс { course_sale / 100 } за 1 000 000\n\n❗ Минимальный заказ 1 000 000 VkCoin\n\n💡 Введите количество коинов для покупки' )
			logic [ ans.from_id ] = 'sale'
			
		elif text in [ '📤Продать', 'продать' ]:
			await ans( f'📤 Купим у тебя коины по курсу:\n{ course / 100 } руб. за 1 000 000.\n\n❗ Минимальное количество койнов: 1 000 000.\n\n💡 Введи количество коинов, которое ты хочешь продать, без пробелов (например, 1000000):' )
			logic [ ans.from_id ] = 'shop'
		
		
	
	else:
		if text.isdigit():
			if ans.from_id in logic:
				if logic[ ans.from_id ] != '':
					if logic[ ans.from_id ] == 'sale':
						await ans( f'💵 К оплате - { int( int( text ) * course_sale ) / 100000000 }₽\n❗Для оплаты перейдите по ссылке https://vk.cc/ax2ngA и укажите комментарий -> ( ans.from_id )\n❗Или произведите оплату с QIWI по этому номеру: ' + str( config.phone ) + ' и укажите комментарий -> ( ans.from_id )' )
						logic [ ans.from_id ] = ''
						po [ ans.from_id ] = text
						op [ ans.from_id ] = int( int( text ) * course_sale ) / 100000000
						
					elif logic[ ans.from_id ] == 'shop':
						await ans( f'💰 Вы получаете { int( int( text ) * course ) / 100000000 }₽ \n❗ Теперь укажите куда будет произведена оплата QIWI ( 79123456789 ): ' )
						logic [ ans.from_id ] = 'shop_qiwi'
						po [ ans.from_id ] = int( text )
						
					elif logic[ ans.from_id ] == 'shop_qiwi':
						await ans( f'💰 Вы получите { int( int( po[ ans.from_id ] ) * course ) / 100000000 } ₽  \❗ Переведите VKC по этой ссылке: { merchant.get_payment_url( amount = po[ ans.from_id ]*1000, payload = 0, free_amount = False ) } ' )
						logic [ ans.from_id ] = ''
						qiwi [ ans.from_id ] = text
						
						

										
						
				else:
					await ans( '❗ Такой команды нет напишите "меню"' )
					
			else:
				await ans( '❗ Такой команды нет напишите "меню"' )
					
		else:
			await ans( '❗ Такой команды нет напишите "меню"' )
			
			
def oplata( ):
	global op
	global po
	trans = api.payments[ 'data' ]
	while True:
		time.sleep( 1 )
		one_trans = api.payments[ 'data' ][ 0 ]
		try:
			if one_trans != trans[ 0 ]:
				if one_trans[ 'comment' ].replace( '\n','').isdigit():

					if int( op[ int( one_trans[ 'comment' ] ) ] ) == one_trans[ 'sum' ][ 'amount' ]:
						merchant.send_payment( to_id = int( one_trans[ 'comment' ] ), amount = int( po[ int( one_trans[ 'comment' ] ) ] ) * 1000 )
						vk.messages.send( message = f'🔥 Вы успешно оплатили всю сумму за { po[ int( one_trans[ "comment" ] ) ] } коинов и коины успешно зачислены на ваш баланс\n💬Оставьте отзыв здесь { otsyv }', random_id = 0, user_id = int( one_trans[ 'comment' ]  ) )
						trans = api.payments[ 'data' ]
						
		except IndexError:
			pass
		
		
t  = threading.Thread( target = oplata, name = 'da', daemon = True, args = () )

t.start()

def opl():
	global po
	global qiwi
	global course
	@merchant.payment_handler( handler_type = 'longpoll' )
	def pay( data ):
		
		api.pay( account = str( qiwi[ data[ 'from_id' ] ] ), amount = int( int( po[ data[ 'from_id' ] ] ) * course ) / 100000000, comment = 'Продажа VKcoin в vk.com/dragonshop101')
		vk.messages.send( message = f'💸 Вы успешно продали { data[ "amount" ] / 1000} вам отправлено { int( int( po[ data["from_id"] ] ) * course ) / 100000000 }₽\n💬 Оставьте свой отзыв здесь { otsyv } ', random_id = 0, user_id = data['from_id'] )
	
	merchant.run_longpoll( tx = [1] )
	
ta = threading.Thread( target = opl, name = 'opl', args = (), daemon = True )

ta.start()

	
bot.run_polling( skip_updates = False )