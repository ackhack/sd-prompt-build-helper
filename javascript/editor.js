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
    active = false;
    max_prompts = -1;
    min_prompts = -1;
}

class PromptModel {
    name = "";
    prompt = "";
    active = true;
    weight = 1;
    loras = [];
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
    static editor = undefined;

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
        if (this.editor === undefined || this.editor === null) {
            this.editor = new ConfigEditor(this.configObject, "pbh-editor");
        } else {
            this.editor.refreshEditor(this.configObject);
        }
    }
}

class ConfigEditor {
    constructor(configObject, containerId) {
        this.container = document.getElementById(containerId);
        this.toggleState = new WeakMap(); // store open/close state per object
        this.refreshEditor(configObject);
    }

    parseValue(val, original) {
        if (typeof original === "number") return Number(val) || 0;
        if (typeof original === "boolean") return !!val;
        return val;
    }

    getArrayItemConstructor(obj, key) {
        if (obj[key].length > 0) {
            const ctor = obj[key][0]?.constructor;
            if (ctor && ctor !== Object) return ctor;
        }

        //workaround as categories is a dup
        if (obj.constructor.name === "CategoryCondition" && key === "categories") {
            return String;
        }

        // Fallback mapping by key
        const classMap = {
            categories: PromptCategory,
            prompts: PromptModel,
            loras: LoraDef,
            tags: String, // For array of strings
        };
        if (classMap[key]) return classMap[key];

        try {
            const defaultInstance = new obj.constructor();
            if (Array.isArray(defaultInstance[key]) && defaultInstance[key].length > 0) {
                const ctor = defaultInstance[key][0]?.constructor;
                if (ctor && ctor !== Object) return ctor;
            }
        } catch {
        }

        return Object;
    }

    applyStyles(element, styles) {
        Object.assign(element.style, styles);
    }

    createToggleButton(isOpen) {
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

    renderObject(obj, container) {
        for (const key in obj) {
            //don't render name or active, except for config itself
            if (obj.constructor.name !== "Config" && key === "active") {
                continue
            }
            if (key === "name") {
                continue
            }
            if (Array.isArray(obj[key])) {
                this.renderArray(obj, key, container);
            } else if (typeof obj[key] === "object" && obj[key] !== null) {
                this.renderObjectField(obj, key, container);
            } else {
                this.renderPrimitiveField(obj, key, container);
            }
        }
    }

    renderArray(obj, key, container) {
        const {wrapper, header, toggleBtn, content} = this.createHtmlContent(obj, key);

        const ctor = this.getArrayItemConstructor(obj, key);
        const ref = new ctor();
        if (typeof ref === "object" && "active" in ref) {
            let toggleAllItemsButton = document.createElement("input");
            toggleAllItemsButton.type = "checkbox";
            toggleAllItemsButton.title = "Toggle All";
            this.applyStyles(toggleAllItemsButton, {
                marginLeft: "6px"
            })
            header.insertBefore(toggleAllItemsButton, header.lastChild);

            toggleAllItemsButton.checked = true;
            for (const arrayItem of obj[key]) {
                if ("active" in arrayItem && !arrayItem.active) {
                    toggleAllItemsButton.checked = false;
                    break;
                }
            }

            toggleAllItemsButton.addEventListener("change", () => {
                for (const arrayItem of obj[key]) {
                    if ("active" in arrayItem) {
                        arrayItem.active = toggleAllItemsButton.checked;
                    }
                }
                this.renderArrayItems(obj[key], content);
            });
        }

        // Add button is outside content, so won't be removed during re-rendering items
        const addBtn = document.createElement("button");
        addBtn.textContent = "Add " + key.slice(0, -1);
        this.applyStyles(addBtn, {marginTop: "8px", cursor: "pointer"});
        wrapper.appendChild(addBtn);

        // Initialize toggle state
        this.setupToggling(obj[key], content, toggleBtn, header);

        // Render initial items
        this.renderArrayItems(obj[key], content);

        addBtn.onclick = () => {
            obj[key].push(new ctor());
            this.renderArrayItems(obj[key], content);
        };

        container.appendChild(wrapper);
    }

    setupToggling(item, content, toggleBtn, header) {
        if (!this.toggleState.has(item))
            this.toggleState.set(item, false);
        const isOpen = this.toggleState.get(item);
        content.style.display = isOpen ? "" : "none";
        toggleBtn.textContent = isOpen ? "▼" : "▶";

        toggleBtn.onclick = () => {
            const current = this.toggleState.get(item);
            this.toggleState.set(item, !current);
            toggleBtn.textContent = !current ? "▼" : "▶";
            content.style.display = !current ? "" : "none";
        };
        header.onclick = () => {
            const current = this.toggleState.get(item);
            this.toggleState.set(item, !current);
            toggleBtn.textContent = !current ? "▼" : "▶";
            content.style.display = !current ? "" : "none";
        };
    }

    createHtmlContent(obj, key) {
        const wrapper = document.createElement("div");
        this.applyStyles(wrapper, {
            border: "1px solid #ccc",
            padding: "8px",
            marginTop: "8px",
            borderRadius: "4px",
        });

        const header = document.createElement("div");
        this.applyStyles(header, {
            display: "flex",
            alignItems: "center",
            cursor: "pointer",
            userSelect: "none",
        });

        const toggleBtn = this.createToggleButton(true);
        header.appendChild(toggleBtn);

        const renderedObject = obj[key];

        if ("active" in renderedObject) {
            const input = this.getInputForProperty(renderedObject, "active");
            header.appendChild(input);
            this.applyStyles(input, {
                marginRight: "6px"
            })
        }

        const title = document.createElement("label");
        title.textContent = this.getCleanTitle(key);
        this.applyStyles(title, {fontWeight: "bold", flexGrow: 1});
        header.appendChild(title);

        wrapper.appendChild(header);

        // Content div contains *only* the array items (no add button)
        const content = document.createElement("div");
        wrapper.appendChild(content);
        return {wrapper, header, toggleBtn, content};
    }

    renderArrayItems(array, container) {
        container.innerHTML = "";

        array.forEach((item, idx) => {
            // Wrap each item in a collapsible container
            const wrapper = document.createElement("div");
            this.applyStyles(wrapper, {
                border: "1px solid #aaa",
                marginTop: "6px",
                borderRadius: "4px",
            });

            const content = document.createElement("div");
            this.applyStyles(content, {padding: "8px"});

            const header = document.createElement("div");
            this.applyStyles(header, {
                display: "flex",
                alignItems: "center",
                cursor: "pointer",
                userSelect: "none",
                padding: "4px 8px",
                fontWeight: "bold",
            });
            wrapper.appendChild(header);
            wrapper.appendChild(content);

            //only add toggling content if item is object
            if (typeof item === "object") {
                const toggleBtn = this.createToggleButton(true);
                header.appendChild(toggleBtn);
                this.setupToggling(item, content, toggleBtn, header);
            }

            // Show a summary title for the item, for example the category's name or just index
            const titleText = item.name || `Item ${idx + 1}`;

            if (item.constructor.name !== "String" && "active" in item) {
                header.appendChild(this.getInputForProperty(item, "active"));
            }

            if (item.constructor.name !== "String" && "name" in item) {
                const input = this.getInputForProperty(item, "name", false);
                header.appendChild(input);
                this.applyStyles(input, {
                    flexGrow: "1",
                });
            } else {
                const title = document.createElement("span");
                title.textContent = titleText;
                this.applyStyles(title, {flexGrow: 1});
                header.appendChild(title);
                this.applyStyles(title, {
                    flexGrow: "1",
                });
            }

            const rightHeader = document.createElement("div");
            header.appendChild(rightHeader);

            let upButton = document.createElement("button");
            upButton.textContent = "↑";
            upButton.onclick = () => {
                if (idx > 0) {
                    let tmp = array[idx - 1];
                    array[idx - 1] = array[idx];
                    array[idx] = tmp;
                    this.renderArrayItems(array, container);
                }
            }
            rightHeader.appendChild(upButton);

            let downButton = document.createElement("button");
            downButton.textContent = "↓";
            downButton.onclick = () => {
                if (idx < array.length - 1) {
                    let tmp = array[idx + 1];
                    array[idx + 1] = array[idx];
                    array[idx] = tmp;
                    this.renderArrayItems(array, container);
                }
            }
            rightHeader.appendChild(downButton);

            if (item.constructor.name === "String") {
                this.renderPrimitiveField(array, idx.toString(), container);
                return;
            } else {
                this.renderObject(item, content);
            }

            const removeBtn = document.createElement("button");
            removeBtn.textContent = "Remove " + titleText;
            this.applyStyles(removeBtn, {
                fontSize: "0.8em",
                marginLeft: "5px",
                marginTop: "5px",
                cursor: "pointer",
            });
            removeBtn.onclick = () => {
                array.splice(idx, 1);
                this.renderArrayItems(array, container);
            };
            content.appendChild(removeBtn);

            container.appendChild(wrapper);
        });
    }

    renderObjectField(obj, key, container) {
        const {wrapper, header, toggleBtn, content} = this.createHtmlContent(obj, key);

        // Initialize toggle state
        this.setupToggling(obj[key], content, toggleBtn, header);

        this.renderObject(obj[key], content);
        container.appendChild(wrapper);
    }

    renderPrimitiveField(obj, key, container) {
        const label = document.createElement("label");
        label.textContent = this.getCleanTitle(key) + ":";
        this.applyStyles(label, {marginTop: "8px", fontWeight: "bold", display: "flex", alignItems: "center"});
        let input;
        if (obj.constructor.name === "PromptCategory" && key === "type") {
            input = this.renderTypeField(obj, key);
        } else {
            input = this.getInputForProperty(obj, key);
        }
        container.appendChild(label);
        label.appendChild(input);
    }

    getInputForProperty(obj, key, standsOut = true) {
        let input = document.createElement("input");
        if (typeof obj[key] === "boolean") {
            input.type = "checkbox";
            input.checked = obj[key];
            this.applyStyles(input, {
                marginLeft: "6px"
            })
            input.addEventListener("change", () => {
                obj[key] = input.checked;
            });
        } else {
            input.value = obj[key];
            this.applyStyles(input, {
                flexGrow: 1,
                padding: "4px",
                marginLeft: "6px"
            });
            if (standsOut) {
                this.applyStyles(input, {
                    border: "1px solid #aaa",
                })
            } else {
                this.applyStyles(input, {
                    backgroundColor: "inherit",
                })
            }
            input.addEventListener("input", () => {
                obj[key] = this.parseValue(input.value, obj[key]);
            });
        }
        return input;
    }

    getCleanTitle(input) {
        input = input.replace(/_/g, " ");
        let words = input.split(" ");
        for (let i = 0; i < words.length; i++) {
            words[i] = words[i].charAt(0).toUpperCase() + words[i].slice(1);
        }
        return words.join(" ");
    }

    renderTypeField(obj, key) {
        // Create select element
        const select = document.createElement('select');

        // Create options
        ['positive', 'negative'].forEach(val => {
            const option = document.createElement('option');
            option.value = val;
            option.textContent = val.charAt(0).toUpperCase() + val.slice(1);
            select.appendChild(option);
            if (obj[key] === val) {
                select.selectedIndex = select.children.length - 1;
            }
        });


        // Change handler
        select.addEventListener('change', () => {
            obj[key] = select.value;
        });

        return select;
    }

    refreshEditor(configObject) {
        this.container.innerHTML = "";
        this.renderObject(configObject, this.container);
    }
}


onUiLoaded(() => {
    PbhEditor.init();
});