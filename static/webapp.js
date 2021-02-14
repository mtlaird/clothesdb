function createNewTagFieldSet() {
    if (checkLastFieldTagSetEmpty()) {
        return;
    }
    let tagFieldsCount = countTagFields();
    let tagFields = document.createElement('p');
    let typeInput = document.createElement('input');
    typeInput.type = 'text';
    typeInput.name = 'tag-type-' + tagFieldsCount.toString();
    typeInput.size = 10;
    typeInput.autocomplete = 'off';
    typeInput.addEventListener('focusout', createNewTagFieldSet);
    let valueInput = document.createElement('input');
    valueInput.type = 'text';
    valueInput.name = 'tag-value-' + tagFieldsCount.toString();
    valueInput.size = 10;
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