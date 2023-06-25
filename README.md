# Yozda Birga Kod Yozamiz Loyihasi uchun Booking System

## installation

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements
python manage.py migrate
python manage.py runserver
```

```
GET /api/rooms
```

Parametrlar:

- `search`: Xona nomi orqali qidirish
- `type`: xona turi bo'yicha saralash (`focus`, `team`, `conference`)
- `page`: sahifa tartib raqami
- `page_size`: sahifadagi maksimum natijalar soni

HTTP 200

```json
{
  "page": 1,
  "count": 3,
  "page_size": 10,
  "results": [
    {
      "id": 1,
      "name": "mytaxi",
      "type": "focus",
      "capacity": 1
    },
    {
      "id": 2,
      "name": "workly",
      "type": "team",
      "capacity": 5
    },
    {
      "id": 3,
      "name": "express24",
      "type": "conference",
      "capacity": 15
    }
  ]
}
```

---

## Xonani id orqali olish uchun API

```
GET /api/rooms/{id}
```

HTTP 200

```json
{
  "id": 3,
  "name": "express24",
  "type": "conference",
  "capacity": 15
}
```

HTTP 404

```json
{
  "detail": "not found"
}
```

---

## Xonaning bo'sh vaqtlarini olish uchun API

```
GET /api/rooms/{id}/availability
```

Parametrlar:

- `date`: sana (ko'rsatilmasa bugungi sana olinadi)

Response 200

```json
[
  {
    "start": "2023-06-19 9:00:00",
    "end": "2023-06-19 11:00:00"
  },
  {
    "start": "2023-06-19 13:00:00",
    "end": "2023-06-19 18:00:00"
  }
]
```

---

## Xonani band qilish uchun API

```
POST /api/rooms/{id}/book
```

```json
{
  "resident": {
    "name": "Anvar Sanayev"
  },
  "start": "2023-06-19 9:00:00",
  "end": "2023-06-19 10:00:00"
}
```

---

HTTP 201: Xona muvaffaqiyatli band qilinganda

```json
{
  "message": "Room successfully booked!"
}
```

HTTP 410: Tanlangan vaqtda xona band bo'lganda

```json
{
  "error": "Booking already exists for the given time period"
}
```
