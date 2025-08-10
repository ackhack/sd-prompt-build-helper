class PbhEditor {

    /** @type {HTMLTableElement} */
    static #table;
    /** @type {HTMLTextAreaElement} */
    static #field;
    /** @type {HTMLButtonElement} */
    static #button;

    /** @param {HTMLDivElement} frame */
    static #constructTable(frame) {
        const table = document.createElement("table");
        const thead = document.createElement('thead');

        const columnWidths = ["15%", "15%", "65%", "5%"];
        const colgroup = document.createElement('colgroup');
        for (const width of columnWidths) {
            const col = document.createElement('col');
            col.style.width = width;
            colgroup.appendChild(col);
        }
        table.appendChild(colgroup);

        const headers = ["Category", "Name", "Prompt", "Del"];
        const thr = thead.insertRow();
        for (const header of headers) {
            const th = document.createElement('th');
            th.textContent = header;
            thr.appendChild(th);
        }
        table.appendChild(thead);

        const tbody = document.createElement('tbody');
        table.appendChild(tbody);
        this.#table = tbody;

        frame.appendChild(table);
    }

    static init() {
        this.#field = document.getElementById("pbh-editor-box").querySelector("textarea");
        this.#button = document.getElementById("pbh-editor-btn");
        this.#constructTable(document.getElementById("pbh-editor"));
    }

    static save() {
        const data = {};
        console.log("save called: " + data);
        this.#field.value = JSON.stringify(data);
        updateInput(this.#field);
        this.#button.click();
    }

    static load() {
        const val = this.#field.value;
        console.log("load called: " + val);
    }
}

onUiLoaded(() => { PbhEditor.init(); });