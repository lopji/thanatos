<?php

namespace hepia\ThanatosBundle\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\Controller;
use hepia\ThanatosBundle\Entity\Data;
use Symfony\Component\Form\Extension\Core\Type\SubmitType;
use Symfony\Component\Form\Extension\Core\Type\TextType;
use Symfony\Component\Form\Extension\Core\Type\FormType;
use Symfony\Component\Form\Extension\Core\Type\ChoiceType;
use Symfony\Component\HttpFoundation\Request;

class SetController extends Controller {

    public function indexAction($page) {
        $max = $this->container->getParameter('max_project_per_page');
        $count = $this->getDoctrine()->getRepository('hepiaThanatosBundle:Data')->countPublishedTotal();
        $pagination = array('page' => $page, 'route' => 'hepia_thanatos_set', 'pages_count' => max(ceil($count / $max), 1), 'route_params' => array());
        $articles = $this->getDoctrine()->getRepository('hepiaThanatosBundle:Data')->getList($page, $max);
        return $this->render('hepiaThanatosBundle:Set:index.html.twig', array('datas' => $articles, 'pagination' => $pagination));
    }

    public function newAction(Request $request) {
        $data = new Data();
        $ip = $this->container->getParameter('ip_server');

        $json = file_get_contents($ip . '/datasets');
        $dataset = (array) json_decode($json);
        
        $formBuilder = $this->get('form.factory')->createBuilder(FormType::class, $data);
        $formBuilder->add('title', TextType::class)
                ->add('description', TextType::class)
                ->add('save', SubmitType::class)
                ->add('dataset', ChoiceType::class, array(
                    'choices' => $dataset));

        $form = $formBuilder->getForm();
        if ($request->isMethod('POST')) {
            $form->handleRequest($request);
            if ($form->isValid()) {
                $em = $this->getDoctrine()->getManager();
                $em->persist($data);
                $em->flush();
                return $this->redirectToRoute('hepia_thanatos_set');
            }
        }
        return $this->render('hepiaThanatosBundle:Set:new.html.twig', array(
                    'form' => $form->createView(),
        ));
    }

    public function viewAction($id) {
        $em = $this->getDoctrine()->getManager();
        $data = $em->getRepository('hepiaThanatosBundle:Data')->find($id);
        if (null === $data) {
            throw new NotFoundHttpException("L'ensemble d'id " . $id . " n'existe pas.");
        }

        return $this->render('hepiaThanatosBundle:Set:view.html.twig', array(
                    'data' => $data
        ));
    }

}
