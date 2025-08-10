/**
 * @template T
 * @param {{ new(): T }} cls - The class constructor to instantiate.
 * @param {string} json - JSON string to parse.
 * @param {object} schema - Mapping for nested class instantiation.
 * @returns {T} - Instance of the given class.
 */
function fromJsonRecursive(cls, json, schema) {
    function revive(obj, currentClass, currentSchema) {
        if (obj === null || typeof obj !== "object") return obj;

        const instance = new currentClass();
        for (const [key, value] of Object.entries(obj)) {
            if (Array.isArray(value) && currentSchema?.[key]?.itemClass) {
                // Array of objects to array of class instances
                instance[key] = value.map(v =>
                    revive(v, currentSchema[key].itemClass, currentSchema[key].schema)
                );
            } else if (currentSchema?.[key]?.class) {
                // Nested object
                instance[key] = revive(value, currentSchema[key].class, currentSchema[key].schema);
            } else {
                // Plain value
                instance[key] = value;
            }
        }
        return instance;
    }

    return revive(JSON.parse(json), cls, schema);
}

class Config {
    active = true;
    base_model = "";
    categories = [];
}

class PromptCategory {
    name = "";
    type = "";
    active = true;
    conditions = new CategoryCondition()
    randomized = new CategoryRandomization()
    prompts = [];
}

class CategoryCondition {
    active = false;
    and_condition = true;
    negative = false;
    tags = [];
    categories = [];
}

class CategoryRandomization {
    randomized = false;
    max_prompts = -1;
    min_prompts = -1;
}

class PromptModel {
    name = "";
    prompt = "";
    active = true;
    loras = [];
    weight = 1;
}

class LoraDef {
    name = "";
    base_model_type = "";
}

// Schema describing which fields are which classes
const schema = {
    categories: {
        itemClass: PromptCategory,
        schema: {
            conditions: {class: CategoryCondition},
            randomized: {class: CategoryRandomization},
            prompts: {
                itemClass: PromptModel,
                schema: {
                    loras: {itemClass: LoraDef}
                }
            }
        }
    }
};
class PbhEditor {
    /** @type {HTMLTextAreaElement} */
    static contentField;
    /** @type {HTMLButtonElement} */
    static saveButton;
    /** @type {Config} */
    static configObject;


    static parseValue(val, original) {
        if (typeof original === "number") return Number(val) || 0;
        if (typeof original === "boolean") return !!val;
        return val;
    }

    static getArrayItemConstructor(obj, key) {
        if (obj[key].length > 0) {
            const ctor = obj[key][0]?.constructor;
            if (ctor && ctor !== Object) return ctor;
        }
        try {
            const defaultInstance = new obj.constructor();
            if (Array.isArray(defaultInstance[key]) && defaultInstance[key].length > 0) {
                const ctor = defaultInstance[key][0]?.constructor;
                if (ctor && ctor !== Object) return ctor;
            }
        } catch {}
        return Object;
    }

    static applyStyles(element, styles) {
        Object.assign(element.style, styles);
    }

    static createToggleButton(isOpen) {
        const btn = document.createElement("button");
        btn.textContent = isOpen ? "▼" : "▶";
        this.applyStyles(btn, {
            background: "none",
            border: "none",
            cursor: "pointer",
            fontWeight: "bold",
            marginRight: "6px",
            padding: "0",
            userSelect: "none",
        });
        return btn;
    }

    static renderObject(obj, container) {
        for (const key in obj) {
            if (Array.isArray(obj[key])) {
                const wrapper = document.createElement("div");
                this.applyStyles(wrapper, {
                    border: "1px solid #ccc",
                    padding: "8px",
                    marginTop: "8px",
                    borderRadius: "4px",
                });

                const header = document.createElement("div");
                this.applyStyles(header, { display: "flex", alignItems: "center", cursor: "pointer", userSelect: "none" });

                const toggleBtn = this.createToggleButton(true);
                const title = document.createElement("label");
                title.textContent = this.getCleanTitle(key);
                this.applyStyles(title, { fontWeight: "bold", flexGrow: 1 });

                header.appendChild(toggleBtn);
                header.appendChild(title);
                wrapper.appendChild(header);

                const content = document.createElement("div");
                wrapper.appendChild(content);

                let open = true;
                toggleBtn.onclick = () => {
                    open = !open;
                    toggleBtn.textContent = open ? "▼" : "▶";
                    content.style.display = open ? "" : "none";
                };

                obj[key].forEach((item, idx) => {
                    const itemDiv = document.createElement("div");
                    this.applyStyles(itemDiv, {
                        marginLeft: "20px",
                        border: "1px solid #ccc",
                        padding: "8px",
                        marginTop: "8px",
                        borderRadius: "4px",
                    });
                    this.renderObject(item, itemDiv);

                    const removeBtn = document.createElement("button");
                    removeBtn.textContent = "Remove " + key.slice(0, -1);
                    this.applyStyles(removeBtn, { fontSize: "0.8em", marginLeft: "5px", marginTop: "5px", cursor: "pointer" });
                    removeBtn.onclick = () => {
                        obj[key].splice(idx, 1);
                        this.refreshEditor();
                    };
                    itemDiv.appendChild(removeBtn);

                    content.appendChild(itemDiv);
                });

                const addBtn = document.createElement("button");
                addBtn.textContent = "Add " + key.slice(0, -1);
                addBtn.onclick = () => {
                    const ctor = this.getArrayItemConstructor(obj, key);
                    obj[key].push(new ctor());
                    this.refreshEditor();
                };
                this.applyStyles(addBtn, { marginTop: "8px", cursor: "pointer" });
                content.appendChild(addBtn);

                container.appendChild(wrapper);

            } else if (typeof obj[key] === "object" && obj[key] !== null) {
                const wrapper = document.createElement("div");
                this.applyStyles(wrapper, {
                    border: "1px solid #ccc",
                    padding: "8px",
                    marginTop: "8px",
                    borderRadius: "4px",
                });

                const header = document.createElement("div");
                this.applyStyles(header, { display: "flex", alignItems: "center", cursor: "pointer", userSelect: "none" });

                const toggleBtn = this.createToggleButton(true);
                const title = document.createElement("label");
                title.textContent = this.getCleanTitle(key);
                this.applyStyles(title, { fontWeight: "bold", flexGrow: 1 });

                header.appendChild(toggleBtn);
                header.appendChild(title);
                wrapper.appendChild(header);

                const content = document.createElement("div");
                wrapper.appendChild(content);

                let open = true;
                toggleBtn.onclick = () => {
                    open = !open;
                    toggleBtn.textContent = open ? "▼" : "▶";
                    content.style.display = open ? "" : "none";
                };

                this.renderObject(obj[key], content);
                container.appendChild(wrapper);

            } else {
                const label = document.createElement("label");
                label.textContent = this.getCleanTitle(key);
                this.applyStyles(label, { display: "block", marginTop: "8px", fontWeight: "bold" });

                let input;
                if (typeof obj[key] === "boolean") {
                    input = document.createElement("input");
                    input.type = "checkbox";
                    input.checked = obj[key];
                    input.style.marginLeft = "6px";
                    input.addEventListener("change", () => {
                        obj[key] = input.checked;
                    });
                    container.appendChild(label);
                    label.appendChild(input); // checkbox inside label for better UX
                } else {
                    input = document.createElement("input");
                    input.value = obj[key];
                    this.applyStyles(input, { width: "300px", padding: "4px" });
                    input.addEventListener("input", () => {
                        obj[key] = this.parseValue(input.value, obj[key]);
                    });
                    container.appendChild(label);
                    container.appendChild(input);
                }
            }
        }
    }

    static getCleanTitle(input){
        input = input.replace(/_/g, " ");
        let words = input.split(" ");
        for (let i = 0; i < words.length; i++) {
            words[i] = words[i].charAt(0).toUpperCase() + words[i].slice(1);
        }
        return " ".join(words);
    }

    static refreshEditor() {
        document.getElementById("pbh-editor").innerHTML = "";
        this.renderObject(this.configObject, document.getElementById("pbh-editor"));
    }

    static init() {
        this.contentField = document.getElementById("pbh-editor-box").querySelector("textarea");
        this.saveButton = document.getElementById("pbh-editor-btn");
        document.getElementById("pbh-editor-load-btn").click();
    }

    static save() {
        console.log("PBH: Save called");
        console.log(this.configObject);
        this.contentField.value = JSON.stringify(this.configObject);
        updateInput(this.contentField);
        this.saveButton.click();
    }

    static load() {
        console.log("PBH: Load called");
        this.configObject = fromJsonRecursive(Config, this.contentField.value, schema)
        this.refreshEditor();
    }
}

onUiLoaded(() => {
    PbhEditor.init();
});