package be.uantwerpen.idlab;

import com.vaadin.annotations.JavaScript;
import com.vaadin.ui.AbstractJavaScriptComponent;
import com.vaadin.ui.JavaScriptFunction;
import elemental.json.JsonArray;

import java.io.Serializable;
import java.util.ArrayList;

@JavaScript({
        "http://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js",
        "gvis.js",
        "gvis-connector.js" })
public class GVis extends AbstractJavaScriptComponent {

    public interface ValueChangeListener extends Serializable {
        void valueChange();
    }

    ArrayList<ValueChangeListener> listeners =
            new ArrayList<ValueChangeListener>();
    public void addListener(ValueChangeListener listener) {
        listeners.add(listener);
    }

    public void setValue(String value) {
        getState().setValue(value);
        markAsDirty();
    }

    public String getValue() {
        return getState().getValue();
    }

    @Override
    public GVisState getState() {
        return (GVisState) super.getState();
    }

    public GVis() {
        addFunction("onClick", new JavaScriptFunction() {
            @Override
            public void call(JsonArray arguments) {
                getState().setValue(arguments.getString(0));
                for (ValueChangeListener listener: listeners)
                    listener.valueChange();
            }
        });
    }

}