# Django–OnlineStore
  
**Version 1.2.6**

> * The functionality of this web–application:
>     *  SignUp; LogIn
>     *  Buy goods; Add money to created account
>     *  View account cart; View top bought goods
>     *  Tests for Django views and DRF views

#### (All comments in code on RUS)

<hr style="border:2px solid gray">

## How to Start

*  __requirements.txt__ in main page
*  Administrator:  
   * Login: __admin__  
   * Password: __admin__
*  Users1:
   * Login: __user__
   * Password: __qaWSed55__
*  Users2:
   * Login: __user2__
   * Password: __qaWSed55__

<hr style="border:2px solid gray">

## Django DRF apps:
## *app_home:*

>Main files; Home page.

<br>

---
## *app_shops:*

>Processes inquiries related to goods.

### *Models:*
*  ### Shop

name |
:---: |
`Char` |

*  ### Goods

name | img | price | amount | shop
:---: | :---: | :---: | :---: | :---:
`Char` | `Image` | `Decimal` | `PositiveInt` | `ForeignKey`<br>`(Shop)`  

*  ### DiscountShop

shop | is_percentage | percentage | money
:---: | :---: | :---: | :---: 
`ForeignKey`<br>`(Shop)` | `Bool` | `PositiveInt` | `PositiveInt`

*  ### DiscountGoods

goods | is_percentage | percentage | money
:---: | :---: | :---: | :---: 
`ForeignKey`<br>`(Goods)` | `Bool` | `PositiveInt` | `PositiveInt`

<br>

---
## *app_users:*

>Processes inquiries related to users.

### *Models:*
*  ### Profile

user | about | money_in_account | amount_spent_money
:---: | :---: | :---: | :---: 
`ForeignKey`<br>`(User)`  | `Char` | `Decimal` | `Decimal`

*  ### ShoppingHistory

profile | goods | price | amount | date
:---: | :---: | :---: | :---: | :---: 
`ForeignKey`<br>`(Pofile)` | `ForeignKey`<br>`(Goods)` | `Decimal` | `PositiveInt` | `Date` 

*  ### ShoppingHistory

profile | goods | amount | add_time
:---: | :---: | :---: | :---: 
`ForeignKey`<br>`(Pofile)` | `ForeignKey`<br>`(Goods)` | `PositiveInt` | `Date` 

<br>
<hr style="border:2px solid gray">

## Contacts
- __Email__: [valery.tychkin@gmail.com](valery.tychkin@gmail.com)  
- __Telegram__: [@ILove1337](https://t.me/ILove1337)
