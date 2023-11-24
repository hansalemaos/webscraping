var elementsToSave = document.querySelectorAll('div[class="ovm-Fixture_Container"]');
var clonedElements = Array.from(elementsToSave).map(el => el.cloneNode(true));
var newDoc = document.implementation.createHTMLDocument('saved_page');
var newBody = newDoc.body;

clonedElements.forEach((el, index) => {
	  var dummyElement0 = document.createElement('div');
  dummyElement0.innerHTML = `<p>ELEMENTSEPSTART${index + 1}</p>`;

  newBody.appendChild(dummyElement0.cloneNode(true));
  newBody.appendChild(el);

  var dummyElement = document.createElement('div');
  dummyElement.innerHTML = `<p>ELEMENTSEPEND${index + 1}</p>`;

  newBody.appendChild(dummyElement.cloneNode(true));
});

var htmlContent = new XMLSerializer().serializeToString(newDoc);
var blob = new Blob([htmlContent], { type: 'text/html' });
var a = document.createElement('a');
a.href = window.URL.createObjectURL(blob);
var timestamp = new Date().toISOString().replace(/[-:]/g, '');
a.download = `saved_page_${timestamp}.html`;
document.body.appendChild(a);
a.click();
document.body.removeChild(a);
