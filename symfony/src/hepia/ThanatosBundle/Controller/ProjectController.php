<?php

namespace hepia\ThanatosBundle\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\Controller;
use hepia\ThanatosBundle\Entity\Project;
use Symfony\Component\Form\Extension\Core\Type\SubmitType;
use Symfony\Component\Form\Extension\Core\Type\TextType;
use Symfony\Component\Form\Extension\Core\Type\FormType;
use Symfony\Component\HttpFoundation\Request;

class ProjectController extends Controller {

    public function indexAction($page) {
        $max = $this->container->getParameter('max_project_per_page');
        $project_count = $this->getDoctrine()->getRepository('hepiaThanatosBundle:Project')->countPublishedTotal();
        $pagination = array('page' => $page, 'route' => 'hepia_thanatos_project', 'pages_count' => max(ceil($project_count / $max), 1), 'route_params' => array());
        $projects = $this->getDoctrine()->getRepository('hepiaThanatosBundle:Project')->getList($page, $max);
        return $this->render('hepiaThanatosBundle:Project:index.html.twig', array('projects' => $projects, 'pagination' => $pagination));
    }

    public function newAction(Request $request) {
        $project = new Project();
        $formBuilder = $this->get('form.factory')->createBuilder(FormType::class, $project);
        $formBuilder->add('title', TextType::class)
                ->add('description', TextType::class)
                ->add('save', SubmitType::class);
        $form = $formBuilder->getForm();
        if ($request->isMethod('POST')) {
            $form->handleRequest($request);
            if ($form->isValid()) {
                $em = $this->getDoctrine()->getManager();
                $em->persist($project);
                $em->flush();
                return $this->redirectToRoute('hepia_thanatos_project');
            }
        }
        return $this->render('hepiaThanatosBundle:Project:new.html.twig', array(
                    'form' => $form->createView(),
        ));
    }

    public function viewAction($id, $page) {
        $em = $this->getDoctrine()->getManager();

        $project = $em->getRepository('hepiaThanatosBundle:Project')->find($id);
        if (null === $project) {
            throw new NotFoundHttpException("Le projet d'id " . $id . " n'existe pas.");
        }

        $max = $this->container->getParameter('max_project_per_page');
        $count = $this->getDoctrine()->getRepository('hepiaThanatosBundle:Instance')->countPublishedTotal($id);
        $pagination = array('page' => $page, 'route' => 'hepia_thanatos_project_view', 'pages_count' => max(ceil($count / $max), 1), 'route_params' => array('id' => $id));
        $instances = $this->getDoctrine()->getRepository('hepiaThanatosBundle:Instance')->getList($id, $page, $max);

        $this->get('hepia.js_vars')->id = $id;

        return $this->render('hepiaThanatosBundle:Project:view.html.twig', array(
                    'project' => $project, 'instances' => $instances, 'pagination' => $pagination
        ));
    }

}
