<?php

namespace hepia\ThanatosBundle\Entity;

use Doctrine\ORM\Mapping as ORM;

/**
 * Instance
 *
 * @ORM\Table(name="instance")
 * @ORM\Entity(repositoryClass="hepia\ThanatosBundle\Repository\InstanceRepository")
 */
class Instance {

    /**
     * @var int
     *
     * @ORM\Column(name="id", type="integer")
     * @ORM\Id
     * @ORM\GeneratedValue(strategy="AUTO")
     */
    private $id;

    /**
     * @var string
     *
     * @ORM\Column(name="title", type="string", length=255)
     */
    private $title;

    /**
     * @var integer
     *
     * @ORM\Column(name="number", type="integer")
     */
    private $number;

    /**
     * @ORM\ManyToOne(targetEntity="hepia\ThanatosBundle\Entity\Project")
     * @ORM\JoinColumn(nullable=false)
     */
    private $project;

    /**
     * @ORM\ManyToOne(targetEntity="hepia\ThanatosBundle\Entity\Network")
     * @ORM\JoinColumn(nullable=false)
     */
    private $network;

    /**
     * @ORM\ManyToOne(targetEntity="hepia\ThanatosBundle\Entity\Data")
     * @ORM\JoinColumn(nullable=false)
     */
    private $data;

    /**
     * Get id
     *
     * @return int
     */
    public function getId() {
        return $this->id;
    }

    /**
     * Set title
     *
     * @param string $title
     *
     * @return Instance
     */
    public function setTitle($title) {
        $this->title = $title;

        return $this;
    }

    /**
     * Get title
     *
     * @return string
     */
    public function getTitle() {
        return $this->title;
    }

    /**
     * Set network
     *
     * @param \hepia\ThanatosBundle\Entity\network $network
     *
     * @return Instance
     */
    public function setNetwork(\hepia\ThanatosBundle\Entity\network $network) {
        $this->network = $network;

        return $this;
    }

    /**
     * Get network
     *
     * @return \hepia\ThanatosBundle\Entity\network
     */
    public function getNetwork() {
        return $this->network;
    }

    /**
     * Set data
     *
     * @param \hepia\ThanatosBundle\Entity\Data $data
     *
     * @return Instance
     */
    public function setData(\hepia\ThanatosBundle\Entity\Data $data) {
        $this->data = $data;

        return $this;
    }

    /**
     * Get data
     *
     * @return \hepia\ThanatosBundle\Entity\Data
     */
    public function getData() {
        return $this->data;
    }

    /**
     * Set project
     *
     * @param \hepia\ThanatosBundle\Entity\Project $project
     *
     * @return Instance
     */
    public function setProject(\hepia\ThanatosBundle\Entity\Project $project) {
        $this->project = $project;

        return $this;
    }

    /**
     * Get project
     *
     * @return \hepia\ThanatosBundle\Entity\Project
     */
    public function getProject() {
        return $this->project;
    }

    /**
     * Set number
     *
     * @param integer $number
     *
     * @return Instance
     */
    public function setNumber($number) {
        $this->number = $number;

        return $this;
    }

    /**
     * Get number
     *
     * @return integer
     */
    public function getNumber() {
        return $this->number;
    }

    public function __clone() {
        $this->id = null;
    }

}
