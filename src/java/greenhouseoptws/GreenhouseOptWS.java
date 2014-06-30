/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package greenhouseoptws;

import com.google.gson.Gson;
import javax.jws.WebMethod;
import javax.jws.WebParam;
import javax.jws.WebService;
import org.python.core.PyFloat;
import org.python.core.PyFunction;
import org.python.util.PythonInterpreter;

/**
 *
 * @author Roxana
 */
@WebService(serviceName = "GreenhouseOptWS")
public class GreenhouseOptWS {

    @WebMethod(operationName = "getCostEfficiency")
    public String getCostEfficiency(@WebParam(name = "json") String json) {
        Request request = new Request();
        Gson gson = new Gson();         
        request = gson.fromJson(json, request.getClass());    

        PythonInterpreter interpret = new PythonInterpreter();
        interpret.execfile("temperature.py");
        PyFloat opt_temp = new PyFloat(request.getOpt_temp());
        PyFloat budget = new PyFloat(request.getBudget());
        PyFloat[] args = {opt_temp, budget};
        PyFunction funct = (PyFunction) interpret.eval("main");
        String result = funct.__call__(args).toString();
        System.out.println(result);
        return result;
    }
}
