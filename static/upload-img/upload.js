/**
 * Show Drag & Drop multiple image preview
 * 
 * @author Anuj Kumar
 * @link https://instagram.com/webtricks.ak
 * @link https://github.com/wtricks
 * */

/** Variables */
let files = [],
dragArea = document.querySelector('.image-uploader'),
input = document.querySelector('.image-uploader input'),
button = document.querySelector('.input-images-1 button'),
select = document.querySelector('.upload-text .select'),
container = document.querySelector('.uploaded');

/** CLICK LISTENER */
select.addEventListener('click', () => input.click());

/* INPUT CHANGE EVENT */
input.addEventListener('change', () => {
	let file = input.files;
    dragArea.classList.remove("form-control");
    dragArea.classList.remove("is-invalid");
    // if user select no image
    if (file.length == 0) return;

	for(let i = 0; i < file.length; i++) {
        if (file[i].type.split("/")[0] != 'image') continue;
        if (!files.some(e => e.name == file[i].name)) files.push(file[i])
    }
    dragArea.classList.add("has-files")

	showImages();
});

function preloaded(){

}


/** SHOW IMAGES */
function showImages() {
    if (files.length == 0){
        dragArea.classList.remove("has-files");
        dragArea.classList.add("form-control");
        dragArea.classList.add("is-invalid")
    }

	container.innerHTML = files.reduce((prev, curr, index) => {
		return `${prev}
		    <div class="uploaded-image">
			    <img src="${URL.createObjectURL(curr)}" />
			    <span class="delIcone" onclick="delImage(${index})">
			    <button class="delete-image"><i class="iui-close"></i></button>
			    </span>
			</div>`
	}, '');
}

/* DELETE IMAGE */
function delImage(index) {
   files.splice(index, 1);
   showImages();
}

/* DRAG & DROP */
dragArea.addEventListener('dragover', e => {
	e.preventDefault()
	dragArea.classList.add('dragover')
})

/* DRAG LEAVE */
dragArea.addEventListener('dragleave', e => {
	e.preventDefault()
	dragArea.classList.remove('dragover')
});

/* DROP EVENT */
dragArea.addEventListener('drop', e => {
	e.preventDefault()
    dragArea.classList.remove('dragover');

	let file = e.dataTransfer.files;
	for (let i = 0; i < file.length; i++) {
		/** Check selected file is image */
		if (file[i].type.split("/")[0] != 'image') continue;
		
		if (!files.some(e => e.name == file[i].name)) files.push(file[i])
	}
	showImages();
});
