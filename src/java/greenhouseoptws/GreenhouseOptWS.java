/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package greenhouseoptws;

import beans.Request;
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
        //wT, wB, T_opt, B_opt, budget, max_T_heat, max_B_light

        Request request = new Request();
        Gson gson = new Gson();
        request = gson.fromJson(json, request.getClass());

        PythonInterpreter interpret = new PythonInterpreter();
        interpret.execfile("cost-efficiency.py");
        PyFloat[] args = {new PyFloat(request.getwT()), new PyFloat(request.getwB()),
            new PyFloat(request.getOpt_temp()), new PyFloat(request.getOpt_bright()),
            new PyFloat(request.getBudget()), new PyFloat(request.getMax_temp_heat()),
            new PyFloat(request.getMax_bright_light())};
        PyFunction funct = (PyFunction) interpret.eval("main");
        String result = funct.__call__(args).asString();
        System.out.println(result);

        return result;
    }
}
