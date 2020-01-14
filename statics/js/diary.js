        let traverseById = (id, node, label) => {
            console.log(node.label);
            console.log(node);
            let childIndex = 0;
            // intentemaos chequiar
            ////console.log(id === node.id);
            if(node.id === id){
                node.label = label;
                return node;
            } else {
                if(!!node.children){
                    node.children.forEach(node=>traverseById(id, node, label));
                }else{
                    return null;
                }
            }
        };
        var vue = new Vue({
            el: '#app',
            delimiters: ["[[", "]]"],
            data: {
                nodes: myNodes,
                defaultProps: {
                    children: 'children',
                    label: 'label',
                    time_spent: "time_spent"
                },
                dialogVisible: false,
                levelsDialogVisible: false,
                saveEnabled: false,
                date: myDate,
                transferDate: null,
                transferType: "mv",
                transferTask: { label: "Na" },
                myArray: myArray,
                expandedNodes: myExpandedNodes,
                levels: myLevels
            },
            methods: {
                save(){
                    console.log("Saving shit");
                    $("#nodes").val(JSON.stringify(this.$data.nodes));
                    $("#notes").val(JSON.stringify(this.$data.myArray));
                    $("#expanded_nodes").val(JSON.stringify(this.$data.expandedNodes));
                    this.$refs.form.submit();
                },
                saveLevels(){
                    console.log("Saving shit");
                    $("#nodes").val(JSON.stringify(this.$data.nodes));
                    $("#notes").val(JSON.stringify(this.$data.myArray));
                    $("#expanded_nodes").val(JSON.stringify(this.$data.expandedNodes));
                    $("#levels").val(JSON.stringify(this.$data.levels));
                    this.$refs.form.submit();
                },
                nodecontext(event, node){
                    console.log("context");
                    console.log(node);
                },
                taskeditname(event, node){
                    this.$data.saveEnabled = true;
                    console.log(node);
                    if(event.target.value!=="")
                        traverseById(node.key, {id: -1, children: this.$data.nodes, label: "root"}, event.target.value);
                },
                append(data) {
                    this.$data.saveEnabled = true;
                    let nodeId = Math.random().toString(36).substr(2, 9);
                    console.log("datatata");

                    if (!!data && this.$data.expandedNodes.indexOf(data.id) === -1)
                        this.$data.expandedNodes.push(data.id);

                    console.log(data);
                    if (!!data) {
                        const newChild = {
                            id: nodeId,
                            label: 'task',
                            time_spent: [null, null],
                            children: []
                        };
                        if (!data.children) {
                            this.$set(data, 'children', []);
                        }
                        data.children.push(newChild);
                    }else{
                        this.$data.nodes.push({
                            id: nodeId,
                            label: 'task',
                            //estimated_time: null,
                            time_spent: [null, null],
                            children: []
                        });
                    }
                    setTimeout(()=>{
                        let label = document.getElementById(nodeId+"_poplabel");
                        console.log(label);
                        label.click();
                    },50);
                },
                remove(node) {
                    this.$data.saveEnabled = true;
                    const parent = node.parent;
                    const children = parent.data.children || parent.data;
                    const index = children.findIndex(d => d.id === node.data.id);
                    children.splice(index, 1);
                },
                taskPopped(nameInputId){
                    let input = document.getElementById(nameInputId+"_name");
                    setTimeout(() => {input.focus();input.select();}, 50);
                },
                afterLeave(nodeId){
                    console.log("After leave");
                    /*
                    let taskName = $("#"+nodeId+"_name").val();
                    console.log(taskName);
                    if(taskName === ""){
                        traverseById(nodeId, {id: -1, children: this.$data.nodes, label: "root"}, "--");
                    }
                    */
                },
                transferConfirm(){
                    console.log(this.$data.transferType);
                    if (this.$data.transferType==="mv"){
                        this.remove(this.$data.transferTask);
                    }
                    $("#nodes").val(JSON.stringify(this.$data.nodes));
                    $("#notes").val(JSON.stringify(this.$data.myArray));
                    $("#expanded_nodes").val(JSON.stringify(this.$data.expandedNodes));
                    $("#transfer").val(JSON.stringify({
                        "node_id": this.$data.transferTask.key,
                        "date": this.$data.transferDate.toISOString().split("T")[0]
                    }));
                    this.$refs.form.submit();
                },
                handleTransferCommand(command, node){
                    if(command==="mcsd"){
                        this.$data.transferTask = node;
                        this.$data.dialogVisible = true;
                    }else{
                        console.log(command);
                        if (command === "mv") {
                            this.remove(node);
                        }
                        $("#nodes").val(JSON.stringify(this.$data.nodes));
                        $("#notes").val(JSON.stringify(this.$data.myArray));
                        $("#expanded_nodes").val(JSON.stringify(this.$data.expandedNodes));
                        $("#transfer").val(JSON.stringify({
                            "node_id": node.key,
                            "date": null
                        }));
                        this.$refs.form.submit();
                    }
                },
                handleDragStart(node, ev) {
                    console.log('drag start', node);
                },
                handleDragEnter(draggingNode, dropNode, ev) {
                    console.log('tree drag enter: ', dropNode.label);
                },
                handleDragLeave(draggingNode, dropNode, ev) {
                    console.log('tree drag leave: ', dropNode.label);
                },
                handleDragOver(draggingNode, dropNode, ev) {
                    console.log('tree drag over: ', dropNode.label);
                },
                handleDragEnd(draggingNode, dropNode, dropType, ev) {
                    console.log('tree drag end: ', dropNode && dropNode.label, dropType);
                },
                handleDrop(draggingNode, dropNode, dropType, ev) {
                    this.$data.saveEnabled = true;
                    console.log('tree drop: ', dropNode.label, dropType);
                },
                allowDrop(draggingNode, dropNode, type) {
                    if (dropNode.data.label === 'Level two 3-1') {
                        return type !== 'inner';
                    } else {
                        return true;
                    }
                },
                allowDrag(draggingNode) {
                    return draggingNode.data.label.indexOf('Level three 3-1-1') === -1;
                },
                dateChange(date){
                    console.log(date.getFullYear(), date.getMonth()+1, date.getDate());
                    window.location = "/diary/"+date.getFullYear()+"-"+(date.getMonth()+1).toString().padStart(2,'0')+"-"+date.getDate().toString().padStart(2,'0');
                },
                newNote(){
                    this.$data.saveEnabled = true;
                    this.$data.myArray.unshift({ id: Math.random().toString(36).substr(2, 9), name: "new note", text: "" })
                },
                deleteNote(noteId){
                    this.$data.saveEnabled = true;
                    let removeIndex = this.$data.myArray.map((item) => item.id).indexOf(noteId);
                    this.$data.myArray.splice(removeIndex, 1);
                },
                editNoteName(noteId){
                    this.$data.saveEnabled = true;
                    let input = document.getElementById(noteId+"_note_name");
                    setTimeout(() => {input.focus();input.select();}, 50);
                },
                noteNameChanged(event, noteId){
                    this.$data.saveEnabled = true;
                    console.log(event.target.value);
                    this.$data.myArray[this.$data.myArray.map((item) => item.id).indexOf(noteId)].name = event.target.value;
                },
                noteTextChanged(event, noteId){
                    this.$data.saveEnabled = true;
                    let newHTML = event.target.innerHTML;
                    let newText = event.target.innerHTML.replace(/<br>/g,"\n");
                    console.log(newText);
                    console.log(event);
                    event.target.innerHTML = "";
                    this.$data.myArray[this.$data.myArray.map((item) => item.id).indexOf(noteId)].text = newText;
                    event.target.innerHTML = newHTML;
                },
                nodeExpanded(node){
                    this.$data.expandedNodes.push(node.id);
                    this.$data.saveEnabled = true;
                },
                nodeCollapsed(node){
                    var index = this.$data.expandedNodes.indexOf(node.id);
                    if (index !== -1) this.$data.expandedNodes.splice(index, 1);
                    this.$data.saveEnabled = true;
                },
                makeLevelsDialogVisible(){
                    console.log("awdawd");
                    this.$data.levelsDialogVisible = true;
                }
            }
        })


