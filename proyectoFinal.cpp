#include <iostream>  //Para entrada y salida estandar
#include <fstream>   //Para operaciones y manipulacion de archivos
#include <vector>    //Para manejar vectores dinamicos
#include <string>    //Para manejar cadenas de texto
#include <algorithm> //Para utilizar sort() y otros algoritmos
#include <sstream>   //Para manejar flujos de texto como cadenas

//Estructura que representa a un estudiante
struct Estudiante {
    std::string nombre; //Almacena el nombre completo del estudiante
    std::string id; //Almacena el ID del estudiante
};

//Funcion que lee datos de estudiantes y los almacena en un vector
bool leerDatosEstudiantes(const std::string& nombreArchivo, std::vector<Estudiante>& estudiantes) {
    std::ifstream archivo(nombreArchivo); //Abre el archivo en modo lectura
    if (!archivo.is_open()) { //Verifica si el archivo se abrio correctamente
        std::cerr << "Error al abrir el archivo de estudiantes." << std::endl;
        return false; //Devuelve false si no se puede abrir el archivo
    }

    std::string linea;
    while (std::getline(archivo, linea)) { //Lee cada linea del archivo
        std::istringstream stream(linea);  //Convierte la linea a un flujo para dividirla
        std::string nombreCompleto, id; //variables para almacenar nombre y ID

        std::getline(stream, nombreCompleto, ':'); //Extrae el nombre antes del caracter ':'
        std::getline(stream, id); //Extrae el ID despues del caracter ':'

        Estudiante est; //Crea un objeto Estudiante
        est.nombre = nombreCompleto; //Asigna el nombre extraido
        est.id = id; //Asigna el ID extraido
        estudiantes.push_back(est);  //Añade el estudiante al vector
    }

    archivo.close(); //Cierra el archivo despues de leerlo
    return true; //Indica éxito
}

//Funcion que lee datos de evaluaciones desde un archivo y los almacena en un vector
bool leerDatosEvaluaciones(const std::string& nombreArchivo, std::vector<std::pair<std::string, double>>& evaluaciones) {
    std::ifstream archivo(nombreArchivo); //abre el archivo en modo lectura
    if (!archivo.is_open()) { //Verifica si el archivo se abrio correctamente
        std::cerr << "Error al abrir el archivo de evaluaciones." << std::endl;
        return false; //devuelve false si hay error
    }

    std::string linea;
    double sumaPorcentajes = 0; //Variable para verificar que los porcentajes sumen a 100%
    while (std::getline(archivo, linea)) {
        std::istringstream stream(linea); //convierte la linea en un flujo de entrada
        std::string nombreEvaluacion; //variable para almacenar el nombre de la evaluacion
        double porcentaje; //variable para almacenar el procentaje

        std::getline(stream, nombreEvaluacion, ':'); //Extrae el nombre de la evaluacion hasta ':'
        stream >> porcentaje; //Extrae el porcentaje de la evaluacion

        evaluaciones.emplace_back(nombreEvaluacion, porcentaje); //Añade la evaluacion al vector
        sumaPorcentajes += porcentaje; //Suma el porcentaje al total
    }

    archivo.close(); //Cierra el archivo

    if (sumaPorcentajes != 100) { //Verifica que la suma sea 100%
        std::cerr << "La suma de los porcentajes no es 100%." << std::endl;
        return false;
    }
    return true; //devuelve true si la operacion fue exitosa
}

//funcion principal del programa
int main() {
    //Variables para almacenar la informacion ingresada por el usuario
    std::string universidad, campus, departamento, semestre, curso, seccion, profesor, nombreArchivoEstudiantes, nombreArchivoEvaluaciones, nombreArchivoCSV;
    int A, B, C, D, F; //variables para almacenar la curva de calificaciones

    //Solicita al usuario informmacion
    std::cout << "Nombre de la Universidad: ";
    std::getline(std::cin, universidad);
    std::cout << "Campus: ";
    std::getline(std::cin, campus);
    std::cout << "Departamento: ";
    std::getline(std::cin, departamento);
    std::cout << "Semestre: ";
    std::getline(std::cin, semestre);
    std::cout << "Curso: ";
    std::getline(std::cin, curso);
    std::cout << "Seccion: ";
    std::getline(std::cin, seccion);
    std::cout << "Nombre del profesor: ";
    std::getline(std::cin, profesor);
    std::cout << "Archivo que contiene los datos de los estudiantes: ";
    std::getline(std::cin, nombreArchivoEstudiantes);
    std::cout << "Archivo con configuracion de evaluaciones: ";
    std::getline(std::cin, nombreArchivoEvaluaciones);
    std::cout << "Curva a utilizar para A, B, C, D, F (ejemplo: A 90 B 80 C 70 D 60 F 0): ";
    std::string curva;
    std::getline(std::cin, curva);

    std::istringstream curvaStream(curva); //Convierte la entrada de la curva en un flujo
    char letra; //variable para almacenar la letra de calificacion
    int valor; //variable para almacenar el valor correspondiente a la calificacion
    while (curvaStream >> letra >> valor) { //procesa los valores de la curva de calificacion
        switch (letra) {
        case 'A': A = valor; break; //asigna valores segun la curva ingresada
        case 'B': B = valor; break;
        case 'C': C = valor; break;
        case 'D': D = valor; break;
        case 'F': F = valor; break;
        }
    }

    std::cout << "Nombre del archivo que contendra al registro de notas: ";
    std::getline(std::cin, nombreArchivoCSV);

    std::ofstream archivo(nombreArchivoCSV); //Crea y abre un archivo para escribir los datos
    if (!archivo.is_open()) { //Verifica si el archivo pudo abrirse correctamente
        std::cerr << "Error al abrir el archivo." << std::endl;
        return 1; //termina el prgrama con codigo de error
    }

    std::vector<Estudiante> estudiantes;
    std::vector<std::pair<std::string, double>> evaluaciones;

    // Verificar datos de estudiantes
    if (!leerDatosEstudiantes(nombreArchivoEstudiantes, estudiantes)) { //Trata de leer los datos de estudiantes desde el archivo
        std::cout << "Desea ingresar otro archivo de estudiantes? (s/n): "; //Pregunta al usuario se desea intentar con otro archivo
        char opcion; //Variable para almacenar la opcion del usuario
        std::cin >> opcion; //Lee la opcion del usuario
        std::cin.ignore(); //Limpia el buffer de entrada para evitar problemas con getLine
        //Bucle que permite al usuario intentar ingresar un nuevo archivo de estudiantes
        while (opcion == 's' || opcion == 'S') { //Mientras el usuario elija s o S
            std::cout << "Ingrese el nuevo archivo de estudiantes: "; //Solicita el nuevo nombre del archivo
            std::getline(std::cin, nombreArchivoEstudiantes); //Lee el nuevo nombre del archivo
            if (leerDatosEstudiantes(nombreArchivoEstudiantes, estudiantes)) { //Intenta leer los datos del nuevo archivo
                break; //Sale del bucle si la lectura es exitosa
            }
            else {
                //Si la lectura falla le dice al usuario y pregunta se desea intentar de nuevo
                std::cout << "Error al abrir el archivo de estudiantes. Intente de nuevo." << std::endl;
                std::cout << "Desea ingresar otro archivo de estudiantes? (s/n): "; //Pregunta nuevamente
                std::cin >> opcion; //Lee la nueva opcion del usuario
                std::cin.ignore(); //Limpiar el buffer
            }
        }
        //Si el usuario decide no seguir intentando termina el programa
        if (opcion != 's' && opcion != 'S') {
            return 1; //Termina el programa con un código de error
        }
    }

    //Ordenar estudiantes alfabeticamente por nombre
    std::sort(estudiantes.begin(), estudiantes.end(), [](const Estudiante& a, const Estudiante& b) {
        return a.nombre < b.nombre; //Compara los nombres de los estudiantes para ordenarlos
        });

    //Verificar datos de evaluaciones
    if (!leerDatosEvaluaciones(nombreArchivoEvaluaciones, evaluaciones)) { //Trata de leer los datos de evaluaciones desde el archivo
        std::cout << "Desea ingresar otro archivo de evaluaciones? (s/n): "; //Pregunta al usuario se desea intentar con otro archivo
        char opcion; //Variable para almacenar la opcion del usuario
        std::cin >> opcion; //Lee la opcion del usuario
        std::cin.ignore(); // Limpiar el buffer
        //Bucle que permite al usuario intentar ingresar un nuevo archivo de evaluaciones
        while (opcion == 's' || opcion == 'S') { //Mientras el usuario elija s o S
            std::cout << "Ingrese el nuevo archivo de evaluaciones: "; //Solicita el nuevo nombre del archivo
            std::getline(std::cin, nombreArchivoEvaluaciones); //Lee el nuevo nombre del archivo
            if (leerDatosEvaluaciones(nombreArchivoEvaluaciones, evaluaciones)) { //Intenta leer los datos del nuevo archivo
                break; // Salir del bucle si la lectura es exitosa
            }
            else {
                //Si la lectura falla le dice al usuario y pregunta se desea intentar de nuevo
                std::cout << "Error al abrir el archivo de evaluaciones. Intente de nuevo." << std::endl;
                std::cout << "Desea ingresar otro archivo de evaluaciones? (s/n): "; //Pregunta nuevamente
                std::cin >> opcion; //Lee la nueva opcion del usuario
                std::cin.ignore(); // Limpiar el buffer
            }
        }
        //Si el usuario decide no seguir intentando termina el programa
        if (opcion != 's' && opcion != 'S') {
            return 1; //Termina el programa con un código de error
        }
    }

    //Informacion general del curso, escribiendo en el archivo CSV
    archivo << ", " << universidad << "\n";
    archivo << ", " << campus << "\n";
    archivo << ", " << departamento << "\n";
    archivo << "Semestre: " << semestre << ", " << "\n";
    archivo << "Profesor: " << profesor << "\n";
    archivo << "Curso: " << curso << "-(" << seccion << ")" << "\n\n";

    archivo << "NUM,NOMBRE,ID"; //Columnas iniciales
    for (const auto& eval : evaluaciones) {
        archivo << "," << eval.first; //Agregar las evaluaciones como encabezado de columna
    }
    archivo << ",AVG,Nota\n"; //Columnas adicionales para promedio y nota final

    //Registro de datos de los estudiantes en el archivo CSV
    int num = 1; //Contador de estudiantes
    int filaInicio = 9; //Numero de fila inicial en la hoja de calculo

    for (const auto& estudiante : estudiantes) { //Itera sobre cada estudiante en la lista
        archivo << num++ << ",\"" << estudiante.nombre << "\"," << estudiante.id; //Escribe el numero de estudiante y nombre
        for (const auto& eval : evaluaciones) { //espacio para calificaciones en las evaluaciones
            archivo << ",";
        }

        //Formula para calcular el promedio en la columna AVG
        std::string formula = "=AVERAGE("; //Inicia la formula de promedio en Excel
        char col = 'D'; //Columna donde comienzan las calificaciones
        for (size_t i = 0; i < evaluaciones.size(); ++i) {
            formula += col + std::to_string(filaInicio) + "*" + std::to_string(evaluaciones[i].second / 100); //Multiplica la calificacion por su peso porcentual
            if (i < evaluaciones.size() - 1) {
                formula += "+"; //agrega signo de suma entre los valores
            }
            col++; //Avanza a la siguientes columna
        }
        formula += ")"; //Cierra la formula

        archivo << "," << formula; //Escribe la formula de promedio en el archivo

        //Escribir la formula de Excel para calcular la calificacion final basada en la curva de notas
        archivo << ",\"=IF(K" << filaInicio << " >= " << A << ", \"\"\A\"\"\,\ IF(K" << filaInicio << " >= " << B << ", \ \"\"\B\"\"\,\ IF(K" << filaInicio << " >= " << C << ", \ \"\"\C\"\"\,\ IF(K" << filaInicio << " >= " << D << ", \ \"\"\D\"\"\,\ \"\"\F\"\"))))\"";
        archivo << "\n"; //salto de linea para el proximo estudiante
        filaInicio++; //Incrementa el numero de fila
    }

    archivo.close(); //Cierra el archivo CSV
    std::cout << "Archivo CSV generado exitosamente: " << nombreArchivoCSV << std::endl; //Mensaje de exito

    return 0; //Fin del programa
}
