# API Response Conventions

2017-09-22 - I've messed up quite a bit and a lot of my API responses are all over the place. A lot of them are a bit too specific to views, so this is a doc to write some more consistent API structures.

1. Instead of returning dictionaries, return list of dictionaries. 

    * The order is apparent.
    * It gives meta information frequently necessary

~~~
result = [
	{
		"key": "key_value",
		"label": "BCAA",
		"value": 55,
		"data_type": "string",
	}
]
~~~

2. Because of #1 never use simple dictionary responses of {k:v}
3. Use ISO for datetime, never use epoch. Use UTC for all time stamps.
4. Use "label" as the string to show the display value
5. Provide data_type so that the frontend has an idea on how to render
6. Try to generally order them by ascending order (you break this rule in too many places). Put more sort filters so that you can deal with this.