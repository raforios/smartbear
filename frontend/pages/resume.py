'''
    Resume Page
'''
import streamlit as st

from layout.menu import menu
from layout.utils import local_css, local_img, local_docs

def abstract():
    image1 = local_img('rrb.png')
    _, col2, _ = st.columns([1, 1, 1])

    rrb = f'''
        <div class="profile-info">
            <h3>Ingeniero de Sistemas, Desarrollador Backend y DevOps</h3>
            <p>
                Soy Ingeniero de Sistemas desde hace más de 20 años, desarrollador de Backend y DevOps conozco lenguajes de programación como Python, Java, JavaScript, C, C++
                y algo de Golang, además de otras herramientas como Shell Script, Bash Script, Terraform, Docker, Kubernetes, HTML, CSS.
            </p>
            <p>
                Desarrollé muchos servicios y micro servicios del tipo API - REST. Tengo mucha experiencia en administración y configuración de
                sistemas operativos Linux en sus versiones Debian, Ubuntu y CentOS. He desarrollado varias automatizaciones e
                integraciones utilizando Shell Scripting y herramientas propias del entorno Unix/Linux.
            </p>
            <p>
                En cuanto a bases de datos, MySQL, PostgreSQL son las que domino y he trabajado la mayor parte de mi carrera, algunas bases del tipo NO SQL como MongoDB y DynamoDB, he
                participado en algunos proyectos con SQL Server y he trabajado como DBA ORACLE y administrador de servidores.
            </p>
        </div>
        '''

    with col2:
        st.image(
            image1,
            width = 300,
            use_container_width = False
        )

    st.write("---")
    st.markdown(rrb, unsafe_allow_html = True)

def content():
    image2 = local_img('about.jpg')
    b64_file = local_docs('cv.pdf')
    _, col2, _ = st.columns([1, 3, 1])

    about = f'''
        <div class="profile-info">
            <h3>Un poco más acerca de mi...</h3>
            <p>
                Tengo un par de diplomados en Tecnologías de la Información y en Educación Superior, también, cuento con una Maestría en Sistemas Flexibles Inteligentes. 
                He realizado cursos de actualización, aprendizaje y capacitación tanto presenciales como virtuales a lo largo de mis 25 años de vida profesional.
            </p>
            <p>
                Soy desarrollador backend desde hace más de 15 años, los lenguajes de programación que conozco más profundamente y que tengo mucha experiencia son Java, Python y JavaScript,
                también conozco Shell Scripting, Bash Scripting, C y C++, tengo conocimientos básicos de Go lang, además conozco algunos lenguajes de Frontend como, HTML y CSS.
            </p>
            <p>
                He trabajado como DevOps y Cloud Computing en AWS, utilizando componentes tales como EC2, ECR, ECS, LAMBDA SERVICES, API GATEWAY, S3, SQS, RDS, IP elásticas y balanceadores de carga y otros. También tengo mucha
                experiencia con Docker y algo de experiencia utilizando Kubernetes. He desarrollado automatizaciones de tareas a través del uso de Shell Scripting y Python. También tengo algo experiencia con GCP y Azure.
            </p>
            <p>
                Tengo mucha experiencia en administración y configuración de sistemas operativos Linux en sus versiones Debian, Ubuntu y CentOS. He desarrollado varias automatizaciones e
                integraciones utilizando Shell Scripting y herramientas propias del entorno Unix/Linux
            </p>
            <p>
                En cuanto a bases de datos, MySQL, PostgreSQL son las que domino y he trabajado la mayor parte de mi carrera, algunas bases del tipo NO SQL como MongoDB y DynamoDB, he
                participado en algunos proyectos con SQL Server y he trabajado como DBA ORACLE y administrador de servidores.
            </p>
            <p>
                He sido catedrático en distintas universidades, me han invitado a asesorar tesis de grado, también he trabajado como capacitador en lenguajes de programación y herramientas tales
                como JavaScript, Node.js, MySQL, Linux, PostgreSQL, Oracle y Java en diferentes institutos.
            </p>
        </div>
        '''
    doc = f'''
        <div class="profile-info">
            <a href="data:application/pdf;base64,{b64_file}" download="Rafael_Rios_Bascon_CV.pdf" class="btn-css">Descarga mi CV</a>
        </div>
        '''

    with col2:
        st.image(
            image2,
            width = 600,
            use_container_width = False
        )

    st.write("---")
    st.markdown(about, unsafe_allow_html = True)
    if b64_file :
        st.markdown(doc, unsafe_allow_html = True)

def contact():
    contact = f'''
        <div class="contact-info">
            <h3 class="title">Contacto:</h3>
            <ul>
                <li>
                    <span class="icon"><a href="https://wa.me/59177781631?text=Consulta%20sobre%20servicios%20de%20desarrollo%20de%20software">
                        <i class="fa-brands fa-whatsapp"></i></a>
                    </span>
                    <span class="text"><a href="https://wa.me/59177781631?text=Consulta%20sobre%20servicios%20de%20desarrollo%20de%20software">
                        +591 777 81631</a>
                    </span>
                </li>
                <li>
                    <span class="icon"><a href="mailto:raforios@gmail.com?Subject=Consulta%20sobre%20servicios">
                        <i class="fa-solid fa-envelope"></i></a>
                    </span>
                    <span class="text"><a href="mailto:raforios@gmail.com?Subject=Consulta%20sobre%20servicios">raforios@gmail.com</a>
                    </span>
                </li>
                <li>
                    <span class="icon"><a href="https://www.linkedin.com/in/raforios" target="_blank">
                        <i aria-hidden="true" class="fa-brands fa-linkedin-in"></i></a>
                    </span>
                    <span class="text"><a href="https://www.linkedin.com/in/raforios" target="_blank">
                        LinkedIn</a>
                    </span>
                </li>
                <li>
                    <span class="icon"><a href="https://github.com/raforios" target="_blank">
                        <i aria-hidden="true" class="fa-brands fa-github"></i></a>
                    </span>
                    <span class="text"><a href="https://github.com/raforios" target="_blank">
                        GitHub</a>
                    </span>
                </li>
            </ul>

        </div>
        '''

    st.markdown(contact, unsafe_allow_html = True)


st.set_page_config(
    page_title = 'Resume Page',
    page_icon = '👤',
    layout = 'wide',
    initial_sidebar_state = 'collapsed'
)

menu()
# local_css('static/css/style.css')
st.markdown('# Rafael R&iacute;os Basc&oacute;n')
st.write("---")
abstract()
st.write("---")
content()
st.write("---")
contact()