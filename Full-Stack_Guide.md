#Django as backend

# Buttons in Dynamic table

_Used for loop to generate icons in each row for each row data_

_Use class not id on each icon to denote same icons on every row. Otherwise duplicate ids will not call event in js, event will be only triggered when icon on 1st row will be clicked._

_Then use querySeletor on js to run event._

2. **Event delegation** - **_Rather than having many event listeners, have one on the parent element. Uses event bubbling._**
	1. I have dynamic rows on table from django, and added buttons on that for loop. So for each row a button appears in that table
	
	2. Create a parent element in which all dynamic or multiple elements will reside.
		```html
		<div class="parent">
			<li class="laptop">1</li>
			<li class="phone">2</li>
			<li class="laptop">3</li>
			...
			<li class="laptop">200</li>	We will not create each eventlistener for each li
		</div>
		```
		
	3. JS-
		```javascript
		const parent = document.querySelector("parent");
		parent.addEventListener("click", (event) => {
			if(event.target.classList.contains("laptop")){
				console.log("clicked laptop");
			}
		}
		```
		**When clicked any child element it's data is present on event. In event.target we can find class/other of the element clicked.**	<br>
		**Here, event's target will have a property 'classList', storing the class of clicked/target element.**

	4. If you have added data attribute in html-
		```html
		<button data-id=1></button>
		```
		
		```javascript
		e.target.dataset.id
		```


