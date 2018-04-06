package be.uantwerpen.idlab;

import com.vaadin.shared.ui.JavaScriptComponentState;

public class GVisState extends JavaScriptComponentState {
    private String value;

    public String getValue() {
        return value;
    }

    public void setValue(String value) {
        this.value = value;
    }
}