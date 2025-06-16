/**
 * Created by Admin on 11-06-2025.
*/
Ext.define('PumpSelection.view.common.buttons.chatbotPanel', {
    extend: 'Ext.panel.Panel',
    xtype: 'chatbotpanel',

    floating: true,
    title: 'PumpSelection Assistant',
    width: 500,
    height: 400,
    closable: true,
    resizable: false,
    layout: 'vbox',
    bodyPadding: 5,
    referenceHolder: true,
    style: {
        zIndex: 9999,
        boxShadow: '0 0 10px rgba(0,0,0,0.3)'
    },
    defaultAlign: 'br-br',

    listeners: {
        afterrender: function (panel) {
            panel.alignTo(Ext.getBody(), 'br-br', [-20, -20]); // bottom-right with offset
            panel.alignTo(Ext.getBody(), 'br-br', [ -320, -420 ]); // added space in between screen bottom-right
        }
    },

    items: [
        {
            xtype: 'dataview',
            reference: 'chatMessages',
            flex: 1,
            scrollable: true,
            itemTpl: '<div style="margin:5px;"><b>{sender}:</b> {message}</div>',
            store: {
                fields: ['sender', 'message'],
                data: [
                    { sender: 'Bot', message: 'Hello! How can I help you in selection ?' },
                    //{ sender: 'Bot', message: 'Plzz, Give me Flow and Head...' }
                ]
            },
            listeners: {
                afterrender: function(dataview) {
                    Ext.defer(() => {
                        dataview.getStore().add({ sender: 'Bot', message: 'Plzz, Give me Flow and Head...' });
                    }, 1000); // 1000ms = 1 second delay
                }
            }
        },
        {
            xtype: 'container',
            layout: 'hbox',
            padding: '5 0 0 5',
            items: [
                {
                    xtype: 'textfield',
                    reference: 'messageInput',
                    flex: 1,
                    emptyText: 'Type a message...',
                    enableKeyEvents: true,
                    listeners: {
                        specialkey: function (field, e) {
                            if (e.getKey() === e.ENTER) {
                                field.up('chatbotpanel').sendMessage();
                            }
                        }
                    }
                },
                {
                    xtype: 'button',
                    text: 'Send',
                    handler: function (btn) {
                        btn.up('chatbotpanel').sendMessage();
                    }
                }
            ]
        }
    ],

    sendMessage: function () {
        var input = this.lookupReference('messageInput');
        var list = this.lookupReference('chatMessages');
        var store = list.getStore();
        var message = input.getValue();

        if (!message.trim()) return;


        // Add user message
        store.add({ sender: 'You', message: message });
        input.reset();

        // Show loading
        store.add({ sender: 'Bot', message: 'Thinking...' });

        let panel = this; // keep reference to current panel

        Ext.Ajax.request({
            url: 'http://localhost:8000/extract',
            method: 'POST',
            jsonData: { text: message },
            timeout: 30000,
            success: function (resp) {
                debugger
                try {
                    var data = Ext.decode(resp.responseText);

                    Ext.Ajax.request({
                        url: UrlManager.selection.getSelections, // ensure this is defined globally
                        method: 'POST',
                        jsonData: data,
                        timeout: 60000,
                        success: function (connection) {
                            debugger
                            try {
                                let jsonData = Ext.decode(connection.responseText);
                                let selectedPumpsJson = Ext.encode(jsonData.data.selectedPumps);

                                Ext.Ajax.request({
                                    url: 'http://localhost:8000/effectivepump',
                                    method: 'POST',
                                    jsonData: selectedPumpsJson,
                                    timeout: 30000,
                                    success: function (resp) {
                                        debugger
                                        try {
                                            let bestEffectivePump = Ext.decode(resp.responseText);
                                            panel.showBotResponse(store, bestEffectivePump);
                                        } catch (decodeError3) {
                                            panel.showBotResponse(store, '❌ Error decoding effective pump result.');
                                        }
                                    },
                                    failure: function () {
                                        panel.showBotResponse(store, '❌ Failed to get effective pump.');
                                    }
                                });

                            } catch (decodeError2) {
                                panel.showBotResponse(store, '❌ Invalid response in selection.');
                            }
                        },
                        failure: function () {
                            panel.showBotResponse(store, '❌ Selection request failed.');
                        }
                    });

                } catch (decodeError1) {
                    panel.showBotResponse(store, '❌ Error decoding extract response.');
                }
            },
            failure: function () {
                panel.showBotResponse(store, '❌ Failed to reach extract endpoint.');
            }
        });
    },

    showBotResponse: function (store, text) {
        // Remove the "Thinking..." placeholder (last message)
        store.removeAt(store.getCount() - 1);

        // Add final response
        store.add({ sender: 'Bot', message: text });

        // Scroll to bottom
        let list = this.lookupReference('chatMessages');
        Ext.defer(() => {
            list.getScrollable().scrollTo(0, list.getScrollable().getMaxPosition().y);
        }, 100);
    }

});