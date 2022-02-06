function createNewTagFieldSet() {
    if (checkLastFieldTagSetEmpty()) {
        return;
    }
    let tagFieldsCount = countTagFields();
    let tagFields = document.createElement('p');
    let typeInput = document.createElement('input');
    typeInput.type = 'text';
    typeInput.name = 'tag-type-' + tagFieldsCount.toString();
    typeInput.size = 15;
    typeInput.autocomplete = 'off';
    typeInput.setAttribute("list", "tag-types-dl");
    typeInput.addEventListener('focusout', tagTypeInputFieldFocusOutHandlerSet);
    let valueInput = document.createElement('input');
    valueInput.type = 'text';
    valueInput.name = 'tag-value-' + tagFieldsCount.toString();
    valueInput.size = 15;
    valueInput.autocomplete = 'off';
    tagFields.append(document.createTextNode("Type: "));
    tagFields.append(typeInput);
    tagFields.append(document.createTextNode(" Value: "));
    tagFields.append(valueInput);
    document.getElementById('tagFieldsContainer').append(tagFields);
}

function countTagFields() {
    let tagFieldsContainer = document.getElementById('tagFieldsContainer');
    return tagFieldsContainer.childNodes.length;
}

function checkLastFieldTagSetEmpty() {
    let lastTagFieldSetNumber = countTagFields() - 1;
    if (lastTagFieldSetNumber < 0) { return false; }
    let lastTypeInputText = document.getElementsByName('tag-type-' + lastTagFieldSetNumber)[0].value;
    let lastValueInputText = document.getElementsByName('tag-value-' + lastTagFieldSetNumber)[0].value;
    return lastTypeInputText === "" && lastValueInputText === "";
}

function tagTypeInputFieldFocusOutHandler(partOfSet, tagTypeValue, tagTypeInputName) {
    if (partOfSet === true) {
        createNewTagFieldSet();
    }
    let tagTypeInputNameArray = tagTypeInputName.split("-");
    let rowNum = tagTypeInputNameArray[tagTypeInputNameArray.length - 1];
    let tagValueInputName = 'tag-value-' + rowNum;
    let valueInput = document.getElementsByName(tagValueInputName)[0];
    let datalistID = 'tag-values-dl-' + tagTypeValue.replace(" ", "_");
    valueInput.setAttribute("list", datalistID);
}

function tagTypeInputFieldFocusOutHandlerSet() {
    return tagTypeInputFieldFocusOutHandler(true, this.value, this.name);
}

function tagTypeInputFieldFocusOutHandlerSingle() {
    return tagTypeInputFieldFocusOutHandler(false, this.value, this.name);
}

function createSingleTagField() {
    let tagFields = document.createElement('p');
    let typeInput = document.createElement('input');
    typeInput.type = 'text';
    typeInput.name = 'tag-type-0';
    typeInput.size = 15;
    typeInput.autocomplete = 'off';
    typeInput.setAttribute("list", "tag-types-dl");
    typeInput.addEventListener('focusout', tagTypeInputFieldFocusOutHandlerSingle);
    let valueInput = document.createElement('input');
    valueInput.type = 'text';
    valueInput.name = 'tag-value-0';
    valueInput.size = 15;
    valueInput.autocomplete = 'off';
    tagFields.append(document.createTextNode("Type: "));
    tagFields.append(typeInput);
    tagFields.append(document.createTextNode(" Value: "));
    tagFields.append(valueInput);
    document.getElementById('singleTagContainer').append(tagFields);
}