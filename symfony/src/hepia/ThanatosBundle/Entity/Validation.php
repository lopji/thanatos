<?php

namespace hepia\ThanatosBundle\Entity;

use Doctrine\ORM\Mapping as ORM;

/**
 * Validation
 *
 * @ORM\Table(name="validation")
 * @ORM\Entity(repositoryClass="hepia\ThanatosBundle\Repository\ValidationRepository")
 */
class Validation {

    /**
     * @var int
     *
     * @ORM\Column(name="id", type="integer")
     * @ORM\Id
     * @ORM\GeneratedValue(strategy="AUTO")
     */
    private $id;

    /**
     * @var float
     *
     * @ORM\Column(name="validation", type="float")
     */
    private $validation;

    /**
     * @var float
     *
     * @ORM\Column(name="training", type="float")
     */
    private $training;

    /**
     * @var int
     *
     * @ORM\Column(name="epoch", type="integer")
     */
    private $epoch;

    /**
     * @var float
     *
     * @ORM\Column(name="accuracy", type="float")
     */
    private $accuracy;

    /**
     * @ORM\ManyToOne(targetEntity="hepia\ThanatosBundle\Entity\Instance")
     * @ORM\JoinColumn(nullable=false)
     */
    private $instance;

    /**
     * Get id
     *
     * @return int
     */
    public function getId() {
        return $this->id;
    }

    /**
     * Set validation
     *
     * @param float $validation
     *
     * @return Validation
     */
    public function setValidation($validation) {
        $this->validation = $validation;

        return $this;
    }

    /**
     * Get validation
     *
     * @return float
     */
    public function getValidation() {
        return $this->validation;
    }

    /**
     * Set training
     *
     * @param float $training
     *
     * @return Validation
     */
    public function setTraining($training) {
        $this->training = $training;

        return $this;
    }

    /**
     * Get training
     *
     * @return float
     */
    public function getTraining() {
        return $this->training;
    }

    /**
     * Set epoch
     *
     * @param integer $epoch
     *
     * @return Validation
     */
    public function setEpoch($epoch) {
        $this->epoch = $epoch;

        return $this;
    }

    /**
     * Get epoch
     *
     * @return int
     */
    public function getEpoch() {
        return $this->epoch;
    }

    /**
     * Set accuracy
     *
     * @param float $accuracy
     *
     * @return Validation
     */
    public function setAccuracy($accuracy) {
        $this->accuracy = $accuracy;

        return $this;
    }

    /**
     * Get accuracy
     *
     * @return float
     */
    public function getAccuracy() {
        return $this->accuracy;
    }


    /**
     * Set instance
     *
     * @param \hepia\ThanatosBundle\Entity\Instance $instance
     *
     * @return Validation
     */
    public function setInstance(\hepia\ThanatosBundle\Entity\Instance $instance)
    {
        $this->instance = $instance;

        return $this;
    }

    /**
     * Get instance
     *
     * @return \hepia\ThanatosBundle\Entity\Instance
     */
    public function getInstance()
    {
        return $this->instance;
    }
}
