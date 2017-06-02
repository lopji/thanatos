<?php

namespace hepia\ThanatosBundle\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\Controller;
use hepia\ThanatosBundle\Entity\Network;
use Symfony\Component\Form\Extension\Core\Type\SubmitType;
use Symfony\Component\Form\Extension\Core\Type\TextType;
use Symfony\Component\Form\Extension\Core\Type\FormType;
use Symfony\Component\Form\Extension\Core\Type\ChoiceType;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpKernel\Exception\NotFoundHttpException;

class NetworkController extends Controller {

    public function indexAction($page) {
        $max = $this->container->getParameter('max_project_per_page');
        $count = $this->getDoctrine()->getRepository('hepiaThanatosBundle:Network')->countPublishedTotal();
        $pagination = array('page' => $page, 'route' => 'hepia_thanatos_network', 'pages_count' => max(ceil($count / $max), 1), 'route_params' => array());
        $articles = $this->getDoctrine()->getRepository('hepiaThanatosBundle:Network')->getList($page, $max);
        return $this->render('hepiaThanatosBundle:Network:index.html.twig', array('networks' => $articles, 'pagination' => $pagination));
    }

    public function newAction(Request $request) {
        $network = new Network();
        $ip = $this->container->getParameter('ip_server');

        $json = file_get_contents($ip . '/networks');
        $architecture = (array) json_decode($json);       
        
        $formBuilder = $this->get('form.factory')->createBuilder(FormType::class, $network);
        $formBuilder->add('title', TextType::class)
                ->add('description', TextType::class)
                ->add('save', SubmitType::class)
                ->add('network', ChoiceType::class, array(
                    'choices' => $architecture
        ));
        $form = $formBuilder->getForm();
        if ($request->isMethod('POST')) {
            $form->handleRequest($request);
            if ($form->isValid()) {
                $em = $this->getDoctrine()->getManager();
                $em->persist($network);
                $em->flush();
                return $this->redirectToRoute('hepia_thanatos_network');
            }
        }
        return $this->render('hepiaThanatosBundle:Network:new.html.twig', array(
                    'form' => $form->createView(),
        ));
    }

    public function viewAction($id) {
        $em = $this->getDoctrine()->getManager();
        $network = $em->getRepository('hepiaThanatosBundle:Network')->find($id);
        if (null === $network) {
            throw new NotFoundHttpException("Le réseau de neurones d'id " . $id . " n'existe pas.");
        }
        return $this->render('hepiaThanatosBundle:Network:view.html.twig', array(
                    'network' => $network
        ));
    }

}
