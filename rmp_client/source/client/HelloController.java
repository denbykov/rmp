package client;

import javafx.fxml.FXML;
import javafx.scene.control.Label;
import javafx.scene.control.TextField;

public class HelloController {
    @FXML
    private TextField name;

    @FXML
    private TextField password;

    @FXML
    protected void UserInformation() {
        System.out.println(name.getText());
        System.out.println(password.getText());
    }
}